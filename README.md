# 📊 Sales & Business Performance Analytics

**An end-to-end data analytics project focused on sales performance, profitability, product analysis, customer segments, and regional business insights using Python and Tableau.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Data%20Analysis-Pandas-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Tableau](https://img.shields.io/badge/Visualization-Tableau-E97627?logo=tableau&logoColor=white)](https://www.tableau.com/)
[![Status](https://img.shields.io/badge/Project-In%20Progress-orange)](https://github.com/faizanusmani20/project-3-sales-business-performance-analytics)

## 📌 Overview

Businesses collect large amounts of sales data, but raw transactions alone do not explain which products perform best, where profits are being generated, or which regions and customer segments need attention.

This project aims to transform raw sales data into a reliable analytical dataset, calculate key business performance indicators (KPIs), identify meaningful trends, and communicate findings through an interactive Tableau dashboard.

The focus is not only on analyzing numbers, but also on translating data into **clear, evidence-based insights that can support business decisions.**

> **Current status:** Data cleaning and initial validation are complete. KPI analysis, exploratory analysis, trend analysis, and the Tableau dashboard are planned next.

## 🎯 Project Objectives

- Clean, validate, and prepare sales data for analysis.
- Measure total sales, profit, order volume, average order value, and profit margin.
- Identify top-performing and potentially underperforming products and categories.
- Analyze monthly, quarterly, and yearly sales and profit trends.
- Compare performance across regions and customer segments.
- Investigate returns, discounts, and loss-making transactions.
- Develop an interactive Tableau dashboard.
- Present evidence-based findings and practical business recommendations.

## 🛠️ Tools & Technologies

| Tool | Purpose |
|---|---|
| Python | Data processing and analysis |
| Pandas | Data cleaning, transformation, and aggregation |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Exploratory data visualization |
| Jupyter Notebook / Google Colab | Analysis environment |
| Tableau | Interactive business dashboard |
| Git & GitHub | Version control and documentation |

## 📂 Dataset Overview

The project uses a Superstore-style sales dataset containing transaction, product, customer, geographical, sales, discount, and profit information.

The source workbook contains three sheets:

| Sheet | Description |
|---|---|
| Orders | Order lines, dates, customers, products, quantities, sales, discounts, and profit |
| People | Regional manager information |
| Returns | Order IDs associated with returned orders |

### Dataset Summary

| Metric | Validated count |
|---|---:|
| Order-line records | 10,194 |
| Distinct orders | 5,111 |
| Regional managers | 4 |
| Returned orders | 296 |
| Order-date coverage | January 2023 – December 2026 |

Each row represents an order line, not necessarily a complete order. Distinct Order IDs must therefore be used when calculating order volume.

*The original dataset's source and usage terms will be documented before final publication.*

## 🧹 Data Cleaning & Validation

The initial cleaning workflow includes:

- Inspecting dataset dimensions, column names, and data types.
- Converting order and shipping dates to datetime format.
- Checking exact duplicate records and distinct order IDs.
- Validating sales, quantity, discount, and profit fields.
- Identifying returned orders using the Returns sheet.
- Mapping regional managers using the People sheet.
- Validating regional mappings and merge consistency.
- Checking row counts, missing values, and date consistency.
- Exporting the cleaned dataset for further analysis.

### Data Quality Principles

- Preserve the original source data.
- Retain legitimate negative-profit transactions.
- Distinguish order lines from distinct orders.
- Document data exclusions and assumptions.
- Validate analytical calculations before presenting results.

## 📊 Business KPIs

The following KPIs will be calculated using consistent definitions across Python and Tableau.

| KPI | Calculation |
|---|---|
| Total Sales | Sum of the documented Sales field |
| Total Profit | Sum of the documented Profit field |
| Order Volume | Count of distinct valid Order IDs |
| Average Order Value | Total Sales ÷ distinct eligible orders |
| Profit Margin | Total Profit ÷ Total Sales × 100 |
| Revenue Growth | (Current-period revenue − Previous comparable-period revenue) ÷ Previous-period revenue × 100 |

Additional analysis will rank products and categories by sales, profit, and quantity, and compare regional and customer segment performance.

Growth calculations will use comparable periods and handle zero or negative comparison-period revenue explicitly.

## 🔍 Planned Analysis

### 1. Exploratory Data Analysis

- Sales and profit distributions.
- Monthly and quarterly performance.
- Product and category contribution.
- Customer segment comparisons.
- Regional performance.
- Discounts, returns, and loss-making transactions.

### 2. Product & Category Performance

- Identify leading products by revenue and quantity.
- Compare revenue contribution with profitability.
- Investigate products or categories with low or negative profit.
- Explore discount patterns where supported by the data.

### 3. Time-Series Analysis

- Examine monthly, quarterly, and yearly sales and profit.
- Compare equivalent reporting periods.
- Investigate potential growth or declining performance.
- Evaluate seasonality only where sufficient historical data is available.

### 4. Regional & Customer Analysis

- Compare sales, profit, and order volume across regions.
- Evaluate customer segment contribution.
- Investigate differences in profitability and growth.
- Develop recommendations supported by validated results.

## 📈 Tableau Dashboard — Coming Soon

The planned dashboard will organize business performance into four views.

| Dashboard page | Planned content |
|---|---|
| Executive Overview | Sales, profit, orders, AOV, margin, and growth |
| Product Performance | Product rankings, category contribution, and profitability |
| Time Trends | Monthly, quarterly, and yearly performance |
| Regional & Customer Analysis | Regional and segment comparisons |

Interactive filters will be included for reporting period, region, category, and customer segment where applicable.

The dashboard preview and workbook will be added to this repository after implementation and validation.

## ⚠️ Data Limitations

- **Future-dated records:** The dataset includes order dates extending beyond the current analysis date. These records require investigation before recent-period trends are interpreted.
- **Order-line granularity:** Row counts are not equivalent to distinct order counts.
- **Returns:** A return indicator identifies returned orders but does not automatically reverse their sales or profit.
- **Profit:** Negative profit values are retained and may represent genuine losses.
- **Seasonality:** Reliable seasonal conclusions require sufficient historical coverage.
- **Business definitions:** The treatment of discounts, returns, costs, taxes, and shipping must follow the available dataset documentation.
- **Causality:** Observed patterns alone do not establish why a business outcome occurred.

These limitations will be considered when interpreting results and preparing recommendations.
<!-- 
## 🗂️ Planned Repository Structure

```text  
project-3-sales-business-performance-analytics/
│
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   ├── 03_kpi_analysis.ipynb
│   └── 04_trend_analysis.ipynb
│
├── src/
│   ├── data_cleaning.py
│   └── kpi_calculations.py
│
├── dashboard/
│
├── reports/
│   └── figures/
│
├── requirements.txt
├── .gitignore
└── README.md
```
-->
*This is the intended structure, not a claim that every listed file already exists. The structure will be updated to match the actual repository as the project progresses.*

## ⚙️ Getting Started

### Prerequisites

- Python 3.9 or later
- Jupyter Notebook or Google Colab
- Git
- Tableau Desktop or Tableau Public for the dashboard stage

### Clone the Repository

```bash
git clone https://github.com/faizanusmani20/project-3-sales-business-performance-analytics.git

cd project-3-sales-business-performance-analytics
```

### Install Dependencies

Once `requirements.txt` has been added and updated with the project's actual dependencies, run:

```bash
pip install -r requirements.txt
```

The analysis notebooks will be documented and added as the workflow develops. Dataset access and paths will be explained alongside the relevant files.

## 📋 Project Roadmap

- [x] Initial data cleaning and validation
- [x] Cleaned dataset exported
- [ ] Exploratory data analysis
- [ ] KPI calculations and validation
- [ ] Product and category analysis
- [ ] Regional and customer segment analysis
- [ ] Trend analysis and business findings
- [ ] Interactive Tableau dashboard
- [ ] Final analytical report and recommendations
- [ ] Project presentation and documentation review

## 👨‍💻 Author

**Faizan Usmani**

Computer Science Student | Aspiring Data Analyst

Interested in Python, data analytics, business intelligence, and data visualization.

- **GitHub:** [faizanusmani20](https://github.com/faizanusmani20)

## 📄 Data Usage

The project code and third-party dataset may be subject to different licensing terms. The dataset's source and redistribution permissions will be checked before the data is published publicly.

---

**Project goal:** Build a reproducible analytics workflow that turns sales data into validated KPIs, meaningful business insights, and practical recommendations.
