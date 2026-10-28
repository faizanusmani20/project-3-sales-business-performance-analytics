# 📊 Sales & Business Performance Analytics

**An end-to-end data analytics project using Python, Pandas, and Tableau to evaluate sales performance, profitability, product performance, customer segments, and regional business results.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Data%20Analysis-Pandas-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Tableau](https://img.shields.io/badge/Visualization-Tableau-E97627?logo=tableau&logoColor=white)](https://www.tableau.com/)
[![Status](https://img.shields.io/badge/Project-In%20Progress-orange)](https://github.com/faizanusmani20/project-3-sales-business-performance-analytics)

## 📌 Project Overview

Raw sales data contains valuable information, but it does not immediately explain which products generate the most profit, which categories underperform, or how different regions and customer segments contribute to business performance.

This project transforms a Superstore-style sales dataset into an analytical resource through data cleaning, validation, KPI calculation, and business performance analysis. The goal is to turn transaction-level data into clear, evidence-based findings that can support business decisions.

The project follows a practical data analytics workflow:

**Data Cleaning → Data Validation → KPI Calculation → Business Analysis → Visualization → Insights & Recommendations**

**Current status:** Data preparation, four KPI calculations, and initial product, category, customer segment, and regional analyses have been completed. Further exploratory analysis, trend analysis, and the Tableau dashboard remain in progress.

## 🎯 Project Objectives

- Prepare a reliable dataset for business analysis.
- Calculate four key performance indicators (KPIs).
- Document the meaning of all 23 dataset columns.
- Compare sales and profitability across product categories and subcategories.
- Identify high-performing and loss-making product areas.
- Evaluate business performance across customer segments and regions.
- Export analytical results into reusable CSV files.
- Develop an interactive Tableau dashboard.
- Communicate findings through a final business report.

## 🛠️ Tools & Technologies

| Tool | Purpose |
|---|---|
| Python | Data processing and analysis |
| Pandas | Data cleaning, aggregation, and KPI calculations |
| NumPy | Numerical operations where required |
| Matplotlib & Seaborn | Exploratory data visualization |
| Jupyter Notebook | Executing and documenting the analysis |
| Tableau | Planned interactive dashboard |
| Git & GitHub | Version control and project documentation |

## 📂 Dataset Overview

The project uses a Superstore-style transactional dataset containing order details, customer information, product classifications, geographical information, sales, discounts, and profit.

The original workbook contains three sheets:

| Sheet | Description |
|---|---|
| Orders | Order lines, dates, customers, products, quantities, sales, discounts, and profit |
| People | Regional manager information |
| Returns | Order IDs associated with returned orders |

### Dataset Summary

| Metric | Value |
|---|---:|
| Order-line records | 10,194 |
| Distinct orders | 5,111 |
| Regional managers | 4 |
| Returned orders | 296 |
| Dataset columns | 23 |

Each row represents an order line, not necessarily a complete order. Therefore, order volume is calculated using distinct `Order ID` values rather than counting rows.

The source dataset contains future-dated records relative to the analysis date. These records have not been silently excluded from the reported KPI results; date-related limitations are documented below.

*The dataset source and applicable redistribution terms should be confirmed before publishing the raw data.*

## 🧹 Data Cleaning & Preparation

The data preparation workflow focuses on improving consistency and making the dataset suitable for analysis.

Key activities include:

- Inspecting dataset dimensions, column names, and data types.
- Checking missing values and duplicate records.
- Converting order and shipping dates to appropriate date formats.
- Validating sales, quantity, discount, and profit fields.
- Reviewing distinct order IDs and order-line granularity.
- Integrating return information using order identifiers.
- Mapping regional managers using the People sheet.
- Validating regional mappings and merge consistency.
- Exporting the prepared dataset for downstream analysis.

### Data Quality Principles

- Preserve the original source data.
- Retain legitimate negative-profit transactions.
- Distinguish order-line records from distinct orders.
- Document assumptions and data limitations.
- Validate calculations before using results in business recommendations.

## 📊 Key Performance Indicators (KPIs)

**Four KPIs have been calculated** using the current `superstore_for_KPI.csv` dataset.

| KPI | Definition | Calculated Result |
|---|---|---:|
| Total Sales | Sum of all values in the Sales field | $2,326,534.35 |
| Total Profit | Sum of all values in the Profit field | $292,296.81 |
| Profit Margin | Total Profit ÷ Total Sales × 100 | 12.56% |
| Total Orders | Count of distinct Order IDs | 5,111 |

### KPI Interpretation

- **Total Sales:** Measures the total recorded sales revenue in the dataset.
- **Total Profit:** Measures the net profit represented by the Profit field.
- **Profit Margin:** Shows the recorded profit as a percentage of sales.
- **Total Orders:** Measures the number of distinct orders, avoiding the overcounting that would result from counting individual order lines.

These results are calculated from the full dataset currently used for KPI analysis. They are not restricted to a selected reporting period.

## 🔍 Business Performance Analysis

Four main areas have been analyzed so far.

### 1. Category Performance

| Category | Sales | Profit |
|---|---:|---:|
| Technology | $839,893.28 | $146,543.38 |
| Furniture | $754,747.76 | $19,730.00 |
| Office Supplies | $731,893.31 | $126,023.44 |

**Initial finding:** Technology has the highest sales and profit among the three categories. Furniture generates substantial sales but considerably lower profit, making its profitability worth investigating further.

### 2. Subcategory Performance

Subcategories have been compared using both sales and profit to avoid judging performance by revenue alone.

| Subcategory | Sales | Profit |
|---|---:|---:|
| Chairs | $335,768.25 | $27,223.53 |
| Phones | $331,842.64 | $45,050.83 |
| Tables | $208,020.18 | -$17,753.21 |
| Binders | $207,354.88 | $31,426.10 |
| Copiers | $150,745.29 | $56,093.94 |
| Bookcases | $115,361.20 | -$3,632.07 |

*Selected subcategories are shown here; the complete subcategory results are available in the exported analysis table.*

**Initial findings:**

- Chairs and Phones are among the leading subcategories by sales.
- Copiers generate the highest profit among the subcategories shown.
- Tables and Bookcases record negative profit despite generating sales.
- High sales do not necessarily indicate high profitability.

### 3. Customer Segment Analysis

| Segment | Sales | Profit | Distinct Orders |
|---|---:|---:|---:|
| Consumer | $1,170,659.79 | $136,371.45 | 2,628 |
| Corporate | $715,806.13 | $94,249.64 | 1,552 |
| Home Office | $440,068.43 | $61,675.73 | 931 |

**Initial finding:** Consumer contributes the highest sales, profit, and order volume among the three segments. Corporate and Home Office also contribute positively to total profit.

### 4. Regional Performance

| Region | Sales | Profit | Distinct Orders |
|---|---:|---:|---:|
| West | $739,813.61 | $110,798.82 | 1,635 |
| East | $691,828.17 | $94,883.26 | 1,475 |
| Central | $503,170.67 | $39,865.31 | 1,179 |
| South | $391,721.90 | $46,749.43 | 822 |

**Initial findings:**

- West records the highest sales and profit among the four regions.
- East is the second-highest region by sales and profit.
- Central has higher sales than South but lower profit.
- Regional performance should be evaluated using both sales and profitability.

These are descriptive findings from the current dataset, not proof of the causes behind business performance.

## 📖 Dataset Column Documentation

A column description table has been created to explain the meaning of the dataset fields.

- **Documented columns:** 23 existing dataset columns.
- **New business-data columns created:** None by the column-description code.
- **Documentation output:** `outputs/column_descriptions.csv`.

The documentation includes fields such as `Order ID`, `Order Date`, `Customer ID`, `Category`, `Sub-Category`, `Sales`, `Quantity`, `Discount`, `Profit`, `Returned`, and `Regional Manager`.

The description table helps teammates understand the data before performing additional analysis. It does not modify the original dataset or add new columns to it.

## 📁 Analysis Outputs

The analysis notebook exports its results as CSV files for reuse in Python, reporting, and the planned Tableau workflow.

| Output file | Contents |
|---|---|
| `outputs/kpi_summary.csv` | Four calculated KPIs |
| `outputs/column_descriptions.csv` | Dataset column names and descriptions |
| `outputs/category_analysis.csv` | Sales and profit by category |
| `outputs/subcategory_analysis.csv` | Sales and profit by subcategory |
| `outputs/segment_analysis.csv` | Sales, profit, and orders by customer segment |
| `outputs/region_analysis.csv` | Sales, profit, and orders by region |

These filenames describe the intended outputs of the notebook. The repository should contain the files that have actually been generated and committed.

## 📈 Tableau Dashboard — Planned

The next visualization stage is an interactive Tableau dashboard based on the validated analytical results.

| Planned dashboard view | Purpose |
|---|---|
| Executive Overview | Display the four KPIs: sales, profit, profit margin, and orders |
| Product Performance | Compare categories and subcategories by sales and profit |
| Customer Segment Analysis | Compare segment contribution and order volume |
| Regional Analysis | Compare regional sales and profitability |
| Trend Analysis | Explore sales and profit over time, after validating date coverage |

Filters for reporting period, region, category, and customer segment may be included where appropriate.

The Tableau workbook, dashboard screenshots, and final insights will be added after implementation and validation.

## 🚀 Project Roadmap

- [x] Inspect and prepare the sales dataset
- [x] Perform initial data validation
- [x] Calculate four business KPIs
- [x] Analyze category and subcategory performance
- [x] Analyze customer segment performance
- [x] Analyze regional performance
- [x] Create dataset column documentation
- [x] Export initial analysis results to CSV
- [ ] Complete exploratory data visualization
- [ ] Validate and analyze time-based trends
- [ ] Develop the interactive Tableau dashboard
- [ ] Write the final business findings and recommendations
- [ ] Add dashboard screenshots and final project documentation




### Run the Analysis

1. Open the KPI and business analysis notebook in Jupyter Notebook.
2. Place the required dataset at the path expected by the notebook.
3. Run the notebook cells in order.
4. Review the KPI summary and analysis tables.
5. Check the generated CSV files in the `outputs/` directory.

The actual dataset filename and dependencies should match the files committed to the repository.

