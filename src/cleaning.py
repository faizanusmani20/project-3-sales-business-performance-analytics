"""Loading, quality checks and cleaning for the Superstore Orders data.

Used by notebooks/01_data_cleaning.ipynb. Produces two files:

* data/interim/orders_clean.csv       every row after cleaning, with flag columns
* data/processed/orders_analysis.csv  the rows used for all analysis (United States only)

The raw workbook in data/raw/ is never modified.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

RAW_FILE_NAME = "sample_-_superstore.xls"
CLEAN_FILE = "data/interim/orders_clean.csv"
ANALYSIS_FILE = "data/processed/orders_analysis.csv"

# Analysis date. Orders dated after it are flagged, not removed (see README, "Assumptions").
REFERENCE_DATE = pd.Timestamp("2026-10-15")

# Only United States rows are analysed; Canadian rows fail several integrity checks (see README).
ANALYSIS_COUNTRY = "United States"

ORIGINAL_COLUMNS = [
    "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode", "Customer ID",
    "Customer Name", "Segment", "Country/Region", "City", "State/Province",
    "Postal Code", "Region", "Product ID", "Category", "Sub-Category",
    "Product Name", "Sales", "Quantity", "Discount", "Profit",
]
ORDER_LEVEL_FIELDS = [
    "Order Date", "Ship Date", "Ship Mode", "Customer ID", "Segment",
    "Country/Region", "City", "State/Province", "Region",
]
TEXT_COLUMNS = [
    "Order ID", "Ship Mode", "Customer ID", "Customer Name", "Segment",
    "Country/Region", "City", "State/Province", "Region", "Product ID",
    "Category", "Sub-Category", "Product Name",
]
CATEGORY_CODES = {"Furniture": "FUR", "Office Supplies": "OFF", "Technology": "TEC"}
COUNTRY_CODES = {"United States": "US", "Canada": "CA"}
DERIVED_COLUMNS = ["Order Year", "Order Quarter", "Order Month", "Shipping Days"]
FLAG_COLUMNS = ["is_returned", "is_future_dated", "in_scope"]
PRICE_TOLERANCE = 0.05   # a line's list price may differ from its product's US price by at most 5%

DATA_DICTIONARY = pd.DataFrame([
    ("Row ID", "integer", "Source line number; unique."),
    ("Order ID", "text", "Order identifier, e.g. US-2023-103800 (country-year-number). One order can have several lines."),
    ("Order Date", "date", "Date the order was placed."),
    ("Ship Date", "date", "Date the order was shipped."),
    ("Ship Mode", "text", "Same Day, First Class, Second Class or Standard Class."),
    ("Customer ID", "text", "Customer identifier; upper-cased during cleaning."),
    ("Customer Name", "text", "Customer name as provided."),
    ("Segment", "text", "Consumer, Corporate or Home Office."),
    ("Country/Region", "text", "United States or Canada (only United States rows are analysed)."),
    ("City", "text", "Shipping city."),
    ("State/Province", "text", "Shipping state or province."),
    ("Postal Code", "text", "US: 5-digit ZIP code (leading zeros restored). Canada: 3-character area prefix only."),
    ("Region", "text", "Central, East, South or West."),
    ("Product ID", "text", "Category code - sub-category code - number. 32 IDs cover more than one product name."),
    ("Category", "text", "Furniture, Office Supplies or Technology."),
    ("Sub-Category", "text", "17 sub-categories, each under one category."),
    ("Product Name", "text", "Product description; repeated spaces collapsed during cleaning."),
    ("Sales", "number", "Line revenue after discount (= list price x Quantity x (1 - Discount)). No currency field; treated as USD."),
    ("Quantity", "integer", "Units on the line."),
    ("Discount", "number", "Fraction taken off the list price, 0 to 0.8."),
    ("Profit", "number", "Line profit as provided; negative for loss-making lines."),
    ("Order Year", "integer", "Derived: year of Order Date."),
    ("Order Quarter", "text", "Derived: quarter of Order Date, e.g. 2023-Q1."),
    ("Order Month", "date", "Derived: first day of the Order Date month."),
    ("Shipping Days", "integer", "Derived: Ship Date - Order Date (time to shipment; there is no delivery date)."),
    ("is_returned", "true/false", "The order is listed in the Returns sheet."),
    ("is_future_dated", "true/false", "Order Date is after the analysis date, 2026-10-15."),
    ("in_scope", "true/false", "United States row; the rows used for all analysis."),
], columns=["Column", "Type", "Description"])


# --------------------------------------------------------------------------- paths
def find_project_root(start: str | Path | None = None) -> Path:
    """Walk up from `start` (default: current folder) to the folder holding src/ and data/."""
    here = Path(start or Path.cwd()).resolve()
    for folder in [here, *here.parents]:
        if (folder / "src").is_dir() and (folder / "data").is_dir():
            return folder
    raise FileNotFoundError("Project root not found: run the notebook from inside the repository.")


# --------------------------------------------------------------------------- loading
def load_raw(path: str | Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Read the Orders and Returns sheets exactly as stored (needs the xlrd package)."""
    orders = pd.read_excel(path, sheet_name="Orders")
    returns = pd.read_excel(path, sheet_name="Returns")
    missing = [c for c in ORIGINAL_COLUMNS if c not in orders.columns]
    if missing:
        raise ValueError(f"Orders sheet is missing columns: {missing}")
    return orders, returns


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with Order Date and Ship Date as datetimes (Excel serial numbers also work)."""
    out = df.copy()
    for col in ["Order Date", "Ship Date"]:
        if pd.api.types.is_numeric_dtype(out[col]):
            out[col] = pd.to_datetime(out[col], unit="D", origin="1899-12-30")
        else:
            out[col] = pd.to_datetime(out[col])
        out[col] = out[col].astype("datetime64[ns]")
    return out


def postal_text(postal: pd.Series) -> pd.Series:
    """Postal codes as text, exactly as stored (numbers lose any trailing '.0')."""
    return postal.astype(str).str.strip().str.replace(r"\.0$", "", regex=True)


# --------------------------------------------------------------------------- diagnostics
def list_price(df: pd.DataFrame) -> pd.Series:
    """Undiscounted unit price implied by a line: Sales / Quantity / (1 - Discount)."""
    return df["Sales"] / df["Quantity"] / (1 - df["Discount"])


def price_mismatch(df: pd.DataFrame) -> pd.Series:
    """True where a line's list price differs by more than 5% from the median US list price
    of the same product (Product ID + Product Name). US prices are the reference because
    every US line matches its product's price."""
    key = ["Product ID", "Product Name"]
    lp = list_price(df)
    us = df["Country/Region"].eq(ANALYSIS_COUNTRY)
    ref = lp[us].groupby([df.loc[us, k] for k in key]).median().rename("ref")
    ref_per_row = df[key].join(ref, on=key)["ref"]
    return ((lp / ref_per_row - 1).abs() > PRICE_TOLERANCE) & ref_per_row.notna()


def copies_of_us_lines(df: pd.DataFrame) -> pd.DataFrame:
    """Canadian lines identical to a US line in every field except Row ID, Order ID prefix
    and location. Returns the matching pairs (index = Canadian row index)."""
    location = ["Row ID", "Order ID", "Country/Region", "City", "State/Province", "Postal Code", "Region"]
    match_cols = [c for c in ORIGINAL_COLUMNS if c not in location]
    us = df[df["Country/Region"].eq(ANALYSIS_COUNTRY)]
    ca = df[df["Country/Region"].eq("Canada")]
    return (ca.reset_index()
              .merge(us[match_cols + ["Order ID"]].drop_duplicates(subset=match_cols),
                     on=match_cols, suffixes=("", " (US)"))
              .set_index("index"))


def quality_checks(orders: pd.DataFrame, returns: pd.DataFrame) -> pd.DataFrame:
    """Run every data-quality check on all rows and on US rows only.

    `orders` must have parsed dates but otherwise be raw. Returns one row per check with
    the count for all rows and for US rows."""
    df = orders
    us_mask = df["Country/Region"].eq(ANALYSIS_COUNTRY)
    rows = []

    def run(group, check, unit, func, detail=""):
        rows.append({"Group": group, "Check": check, "Unit": unit,
                     "All rows": int(func(df)), "US rows": int(func(df[us_mask])), "Detail": detail})

    dup_cols = [c for c in ORIGINAL_COLUMNS if c != "Row ID"]
    run("Completeness", "Missing values", "cells", lambda d: d[ORIGINAL_COLUMNS].isna().sum().sum())
    run("Duplicates", "Repeated Row IDs", "rows", lambda d: d["Row ID"].duplicated().sum())
    run("Duplicates", "Lines repeating another line (all columns except Row ID)", "lines",
        lambda d: d.duplicated(subset=dup_cols).sum(), "the second copy of each pair")

    for f in ORDER_LEVEL_FIELDS:
        run("Consistency", f"Orders with more than one {f}", "orders",
            lambda d, f=f: (d.groupby("Order ID")[f].nunique() > 1).sum())

    def oid_parts(d):
        return d["Order ID"].str.extract(r"^(?P<prefix>[A-Z]{2})-(?P<year>\d{4})-(?P<num>\d+)$")
    run("Consistency", "Order IDs not in the form XX-YYYY-NNNNNN", "lines", lambda d: oid_parts(d)["prefix"].isna().sum())
    run("Consistency", "Order ID year differs from Order Date year", "lines",
        lambda d: (pd.to_numeric(oid_parts(d)["year"]) != d["Order Date"].dt.year).sum())
    run("Consistency", "Order ID prefix does not match the country", "lines",
        lambda d: (oid_parts(d)["prefix"] != d["Country/Region"].map(COUNTRY_CODES)).sum())
    run("Consistency", "Order numbers reused in a different year", "order numbers",
        lambda d: (oid_parts(d.drop_duplicates("Order ID")).groupby("num")["year"].nunique() > 1).sum())

    def pid_parts(d):
        return d["Product ID"].str.extract(r"^(?P<cat>[A-Z]{3})-(?P<sub>[A-Z]{2})-\d+$")
    run("Consistency", "Product ID category code does not match Category", "lines",
        lambda d: (pid_parts(d)["cat"] != d["Category"].map(CATEGORY_CODES)).sum())
    run("Consistency", "Sub-categories whose Product IDs use more than one code", "sub-categories",
        lambda d: (pid_parts(d)["sub"].groupby(d["Sub-Category"]).nunique() > 1).sum())
    run("Consistency", "Sub-categories listed under more than one Category", "sub-categories",
        lambda d: (d.groupby("Sub-Category")["Category"].nunique() > 1).sum())
    run("Consistency", "Customer IDs with more than one name", "customer IDs",
        lambda d: (d.groupby("Customer ID")["Customer Name"].nunique() > 1).sum())
    run("Consistency", "Customer names with more than one Customer ID", "names",
        lambda d: (d.groupby("Customer Name")["Customer ID"].nunique() > 1).sum())
    run("Consistency", "Ship Date before Order Date", "lines", lambda d: (d["Ship Date"] < d["Order Date"]).sum())
    run("Consistency", "Lines priced more than 5% away from the product's US price", "lines",
        lambda d: price_mismatch(df)[d.index].sum(), "list price = Sales / Quantity / (1 - Discount)")
    run("Consistency", "Canadian lines identical to a US line", "lines",
        lambda d: d.index.isin(copies_of_us_lines(df).index).sum(), "all fields equal except the location")

    run("Value range", "Quantity below 1", "lines", lambda d: (d["Quantity"] < 1).sum())
    run("Value range", "Sales of zero or less", "lines", lambda d: (d["Sales"] <= 0).sum())
    run("Value range", "Discount outside 0 to below 1", "lines", lambda d: (~d["Discount"].between(0, 1, inclusive="left")).sum())
    run("Value range", "Profit greater than Sales", "lines", lambda d: (d["Profit"] > d["Sales"]).sum())

    run("Text", "Text values with leading or trailing spaces", "values",
        lambda d: sum((d[c].astype(str) != d[c].astype(str).str.strip()).sum() for c in TEXT_COLUMNS))
    run("Text", "Product names containing repeated spaces", "names",
        lambda d: d.loc[d["Product Name"].str.contains("  ", regex=False), "Product Name"].nunique())
    run("Text", "Customer IDs containing lowercase letters", "customer IDs",
        lambda d: d.loc[d["Customer ID"].str.contains("[a-z]", regex=True), "Customer ID"].nunique())
    run("Keys", "Product IDs used for more than one product name", "product IDs",
        lambda d: (d.groupby("Product ID")["Product Name"].nunique() > 1).sum(),
        "different products share an ID; product analysis uses ID + name")

    pc = postal_text(df["Postal Code"])
    run("Postal code", "US ZIP codes missing their leading zero", "lines",
        lambda d: (d["Country/Region"].eq(ANALYSIS_COUNTRY) & pc[d.index].str.fullmatch(r"\d{1,4}")).sum())
    run("Postal code", "Canadian postal codes holding only the 3-character area prefix", "lines",
        lambda d: (d["Country/Region"].eq("Canada") & (pc[d.index].str.len() == 3)).sum())

    ret_ids = set(returns["Order ID"])
    run("Returns", "Returned Order IDs not found in Orders", "order IDs",
        lambda d: len(ret_ids - set(d["Order ID"])))
    run("Returns", "Lines belonging to a returned order", "lines", lambda d: d["Order ID"].isin(ret_ids).sum())
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- cleaning
def clean(orders: pd.DataFrame, returns: pd.DataFrame,
          reference_date: pd.Timestamp = REFERENCE_DATE) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply every cleaning rule. Returns (cleaned rows with flags, cleaning log).

    No values are invented and no rows are dropped except exact repeat lines."""
    df = parse_dates(orders)
    log = []

    def step(name, rows_before, rows_after, changed, note):
        log.append({"Step": name, "Rows before": rows_before, "Rows after": rows_after,
                    "Values changed": int(changed), "Note": note})

    n = len(df)
    # 1. Text: trim and collapse repeated spaces
    changed, touched = 0, []
    for c in TEXT_COLUMNS:
        new = df[c].astype(str).str.strip().str.replace(r"\s{2,}", " ", regex=True)
        k = int((new != df[c]).sum())
        if k:
            changed += k
            touched.append(f"{c}: {k}")
        df[c] = new
    step("Trim text and collapse repeated spaces", n, n, changed, "cosmetic; " + (", ".join(touched) or "no changes"))

    # 2. Customer IDs in upper case (only if that does not merge two different customers)
    upper = df["Customer ID"].str.upper()
    clash = (pd.DataFrame({"orig": df["Customer ID"], "up": upper}).drop_duplicates()
             .groupby("up")["orig"].nunique() > 1)
    if clash.any():
        raise ValueError(f"Upper-casing would merge Customer IDs: {list(clash[clash].index)}")
    step("Customer ID to upper case", n, n, (upper != df["Customer ID"]).sum(),
         ", ".join(sorted(df.loc[upper != df["Customer ID"], "Customer ID"].unique())))
    df["Customer ID"] = upper

    # 3. Postal codes as text; US ZIP codes back to 5 digits
    pc = postal_text(df["Postal Code"])
    short = df["Country/Region"].eq(ANALYSIS_COUNTRY) & pc.str.fullmatch(r"\d{1,4}")
    df["Postal Code"] = pc.where(~short, pc.str.zfill(5))
    step("Postal Code to text; leading zero restored on US ZIP codes", n, n, short.sum(),
         "states: " + ", ".join(sorted(df.loc[short, "State/Province"].unique())))

    # 4. Remove exact repeat lines (every column equal except Row ID); keep the first copy
    dup_cols = [c for c in ORIGINAL_COLUMNS if c != "Row ID"]
    repeat = df.duplicated(subset=dup_cols, keep="first")
    removed = df.loc[repeat, ["Row ID", "Order ID"]]
    df = df.loc[~repeat].copy()
    step("Remove exact repeat lines", n, len(df), repeat.sum(),
         "removed Row IDs " + ", ".join(f"{r} ({o})" for r, o in removed.itertuples(index=False)))

    # 5. Derived columns
    df["Order Year"] = df["Order Date"].dt.year.astype("int64")
    df["Order Quarter"] = df["Order Date"].dt.to_period("Q").astype(str).str.replace("Q", "-Q", regex=False)
    df["Order Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp().astype("datetime64[ns]")
    df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days.astype("int64")
    step("Add Order Year, Order Quarter, Order Month, Shipping Days", len(df), len(df), 0,
         "Shipping Days = Ship Date - Order Date (order to shipment, not delivery)")

    # 6. Flags
    df["is_returned"] = df["Order ID"].isin(set(returns["Order ID"]))
    step("Flag lines of returned orders (is_returned)", len(df), len(df), df["is_returned"].sum(),
         f"{df.loc[df['is_returned'], 'Order ID'].nunique()} orders in the Returns sheet")
    df["is_future_dated"] = df["Order Date"] > reference_date
    step("Flag lines dated after the analysis date (is_future_dated)", len(df), len(df), df["is_future_dated"].sum(),
         f"Order Date after {reference_date.date()}")
    df["in_scope"] = df["Country/Region"].eq(ANALYSIS_COUNTRY)
    step("Flag analysis scope (in_scope = United States)", len(df), len(df), (~df["in_scope"]).sum(),
         "Canadian rows set to out of scope")

    df = df[ORIGINAL_COLUMNS + DERIVED_COLUMNS + FLAG_COLUMNS].reset_index(drop=True)
    validate_clean(df)
    return df, pd.DataFrame(log)


def validate_clean(df: pd.DataFrame) -> None:
    """Fail loudly if a cleaned table breaks a rule the analysis relies on."""
    scope = df[df["in_scope"]]
    problems = []
    if df[ORIGINAL_COLUMNS].isna().any().any():
        problems.append("missing values")
    if df.duplicated(subset=[c for c in ORIGINAL_COLUMNS if c != "Row ID"]).any():
        problems.append("exact repeat lines")
    if (df["Shipping Days"] < 0).any():
        problems.append("ship date before order date")
    for f in ORDER_LEVEL_FIELDS:
        if (scope.groupby("Order ID")[f].nunique() > 1).any():
            problems.append(f"in-scope orders with more than one {f}")
    if not scope["Postal Code"].str.fullmatch(r"\d{5}").all():
        problems.append("in-scope postal codes that are not 5 digits")
    if price_mismatch(df)[df["in_scope"]].any():
        problems.append("in-scope lines with inconsistent prices")
    if problems:
        raise ValueError("Cleaned data failed validation: " + "; ".join(problems))


def analysis_set(clean_df: pd.DataFrame) -> pd.DataFrame:
    """Rows used for EDA and KPIs: in scope (United States)."""
    return clean_df[clean_df["in_scope"]].reset_index(drop=True)


# --------------------------------------------------------------------------- saving / loading
def save_csv(df: pd.DataFrame, path: str | Path) -> None:
    out = df.copy()
    for c in ["Order Date", "Ship Date", "Order Month"]:
        if c in out:
            out[c] = out[c].dt.strftime("%Y-%m-%d")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(path, index=False)


def load_clean(path: str | Path) -> pd.DataFrame:
    """Read a cleaned CSV back with the right types (Postal Code stays text)."""
    df = pd.read_csv(path, dtype={"Postal Code": str, "Customer ID": str, "Order Quarter": str},
                     parse_dates=["Order Date", "Ship Date", "Order Month"],
                     float_precision="round_trip")   # read Sales/Profit back bit-for-bit
    for c in ["Order Date", "Ship Date", "Order Month"]:
        df[c] = df[c].astype("datetime64[ns]")
    for c in FLAG_COLUMNS:
        if c in df:
            df[c] = df[c].astype(bool)
    return df
