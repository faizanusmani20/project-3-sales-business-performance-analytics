# Sales & Business Performance Analytics: Superstore

Analysis of a retail order dataset to measure revenue, profit, order volume and growth; find the products, regions and customer segments that drive or drain performance; and feed a Power BI dashboard.

## Progress

- [x] Week 1: data cleaning and validation (`notebooks/01_data_cleaning.ipynb`)
- [x] Week 1: exploratory data analysis (`notebooks/02_eda.ipynb`)
- [ ] Week 2: KPI calculation and product, customer and region analysis (`notebooks/03_kpis.ipynb`)
- [ ] Week 3: trend analysis and business insights
- [ ] Week 4: Power BI dashboard, final report and presentation

## Repository structure

```
superstore-sales-analytics/
├── data/
│   ├── raw/sample_-_superstore.xls        source workbook (never edited)
│   ├── interim/orders_clean.csv           every row after cleaning, with flag columns
│   └── processed/
│       ├── orders_analysis.csv            analysis set: United States order lines
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
├── reports/
│   ├── data_quality_checks.csv, cleaning_log.csv, data_dictionary.csv
│   └── figures/                           charts saved by the EDA notebook
├── src/
│   ├── cleaning.py                        loading, quality checks, cleaning rules
│   ├── checks.py                          claim checks used at the end of each notebook
│   ├── viz.py                             shared chart style
│   └── __init__.py
├── requirements.txt
└── README.md
```

## Setup

Requires Python 3.9 or later (tested on 3.11 and 3.13).

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook
```

Run the notebooks **in order**: each one reads the files written by the one before. Each notebook ends with a claim-verification cell that recomputes every number quoted in its summary and stops with an error if any of them no longer matches the data.

**Google Colab:** clone the repository, then run the notebooks from inside it:

```python
!git clone https://github.com/<your-account>/<this-repo>.git
%cd <this-repo>/notebooks
```

## Data source

- **File:** `data/raw/sample_-_superstore.xls`, the "Sample - Superstore" retail dataset published by Tableau as sample data. This copy covers orders dated 3 January 2023 to 30 December 2026.
- **Sheets:**
  - **Orders:** 10,194 rows × 21 columns. One row is one **order line**; there are 5,111 orders.
  - **Returns:** 296 returned Order IDs.
  - **People:** regional managers; not used.
- The raw file is never edited. All changes are made in code (`src/cleaning.py`) and written to new files.

## Scope and assumptions

- **United States only.** The 200 Canadian rows fail the integrity checks that every US row passes:
  - 37% of them carry another product's price.
  - 14 lines copy US orders line for line.
  - 29 of 63 Canadian order numbers reappear in another year.
  - One customer has five IDs inside a single order.

  They are kept in `data/interim/orders_clean.csv` with `in_scope = False`. Notebook 01 (section 4) shows the evidence and their effect on product results.
- **Gross figures:** sales and profit include returned orders unless a figure is labelled *net*. The Returns sheet lists whole orders without amounts, so net figures treat a returned order as fully returned.
- **Dates:** the analysis date is **15 October 2026**. The 1,069 US lines dated after it are kept and flagged (`is_future_dated`) so 2026 can be compared as a full year; 2026 is also compared like for like (1 January–15 October) with 2025.
- **Currency:** there is no currency field; amounts are treated as US dollars.
- **Sales** are after discount (list price × quantity × (1 − discount)). **Profit** is used as provided.
- **Shipping Days** = Ship Date − Order Date, i.e. the time to shipment. The data has no delivery date.

## Cleaning rules

| Rule | Rows affected |
|---|---|
| Trim text and collapse repeated spaces | 7 product names (32 lines) |
| Upper-case Customer IDs (checked: no two customers merge) | 3 IDs (43 lines) |
| Postal Code stored as text; leading zero restored on US ZIP codes | 438 lines (CT, ME, MA, NH, NJ, RI) |
| Remove exact repeat lines (identical in every column except Row ID) | 2 lines (Row IDs 392 and 1700) |
| Add Order Year, Order Quarter, Order Month, Shipping Days | all rows |
| Flag `is_returned`, `is_future_dated`, `in_scope` | 800, 1,093 and 199 out-of-scope rows |

No values are estimated or filled, because there are no missing values. Every raw line is accounted for: analysis set (9,993) + Canadian rows (199) + removed repeats (2) = 10,194, and sales, profit and quantity reconcile exactly.

**Known issue kept as is:** 32 Product IDs cover more than one product name, so product analysis identifies a product by Product ID + Product Name.

## Data dictionary

| Column | Type | Description |
|---|---|---|
| Row ID | integer | Source line number; unique. |
| Order ID | text | Order identifier, e.g. US-2023-103800 (country-year-number). One order can have several lines. |
| Order Date | date | Date the order was placed. |
| Ship Date | date | Date the order was shipped. |
| Ship Mode | text | Same Day, First Class, Second Class or Standard Class. |
| Customer ID | text | Customer identifier; upper-cased during cleaning. |
| Customer Name | text | Customer name as provided. |
| Segment | text | Consumer, Corporate or Home Office. |
| Country/Region | text | United States or Canada (only United States rows are analysed). |
| City | text | Shipping city. |
| State/Province | text | Shipping state or province. |
| Postal Code | text | US: 5-digit ZIP code (leading zeros restored). Canada: 3-character area prefix only. |
| Region | text | Central, East, South or West. |
| Product ID | text | Category code - sub-category code - number. 32 IDs cover more than one product name. |
| Category | text | Furniture, Office Supplies or Technology. |
| Sub-Category | text | 17 sub-categories, each under one category. |
| Product Name | text | Product description; repeated spaces collapsed during cleaning. |
| Sales | number | Line revenue after discount (= list price x Quantity x (1 - Discount)). No currency field; treated as USD. |
| Quantity | integer | Units on the line. |
| Discount | number | Fraction taken off the list price, 0 to 0.8. |
| Profit | number | Line profit as provided; negative for loss-making lines. |
| Order Year | integer | Derived: year of Order Date. |
| Order Quarter | text | Derived: quarter of Order Date, e.g. 2023-Q1. |
| Order Month | date | Derived: first day of the Order Date month. |
| Shipping Days | integer | Derived: Ship Date - Order Date (time to shipment; there is no delivery date). |
| is_returned | true/false | The order is listed in the Returns sheet. |
| is_future_dated | true/false | Order Date is after the analysis date, 2026-10-15. |
| in_scope | true/false | United States row; the rows used for all analysis. |

## Exploratory findings (notebook 02)

*US order lines, gross of returns, including lines dated after 15 October 2026.*

- Sales are **$2.30M** and profit **$286K**, a **12.5% margin**. 18.7% of lines lose money, and line values are heavily skewed (median $54, mean $230).
- **Furniture** is second in sales ($742K) but earns only a 2.5% margin. Technology (17.4%) and Office Supplies (17.0%) are healthy.
- Only **Tables, Bookcases and Supplies** lose money. Tables lose the most: −$17.7K on $207K of sales, with a 26.1% average discount. Machines earn just 1.8%. Copiers rank 8th in sales but earn the most profit.
- **Discounts:** margin is 29.5% with no discount, positive up to a 20% discount, and negative at every level of 30% or more. Lines discounted 30% or more (13.9% of lines) lose $135K. This is an association: discount levels differ by region and product.
- **Seasonality:** September, November and December are the top sales months every year; September–December brings 50–54% of annual sales.
- **Regions:** West and East bring 61.1% of sales and 69.8% of profit. Central has the lowest margin (7.9%) and the highest average discount (24.0%).
- **Shipping:** Standard Class averages 5.0 days to shipment and First Class 2.2 days; 95.6% of Same Day lines ship on the order date.

Charts are in `reports/figures/`.

## Limitations

- The dataset is a published sample, not live data. 1,069 US lines are dated after the analysis date, and all 2026 figures for 16 October onwards depend on them.
- The Returns sheet has no amounts or dates, so net figures assume each returned order was fully returned.
- There is no cost, tax, shipping-charge, currency or sales-channel field. Profit cannot be recomputed and channel analysis is not possible.
- Relationships found (for example between discount and profit) are associations, not proof of cause.
