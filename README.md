# Sales & Business Performance Analytics Dashboard

An end-to-end data analytics project focused on analyzing sales, profitability, product performance, customer segments, and regional trends using the **Sample Superstore Dataset**. The project uses Python for data cleaning and exploratory data analysis (EDA), and Microsoft Power BI for interactive business intelligence and visualization.

## Project Overview

The objective of this project is to transform raw transactional sales data into meaningful business insights that can support data-driven decision-making.

The analysis focuses on identifying sales trends, evaluating profitability, understanding customer purchasing behavior, and detecting products or regions that require business attention.

## Objectives

- Clean and prepare raw sales data for analysis.
- Calculate key business performance indicators (KPIs).
- Analyze sales and profit trends over time.
- Evaluate product and category-level performance.
- Compare regional and customer-segment performance.
- Investigate the relationship between discounts and profitability.
- Build an interactive Power BI dashboard.
- Provide actionable business recommendations based on analytical findings.

## Dataset

**Dataset:** Sample Superstore

The dataset contains transactional retail sales information, including:

| Attribute | Description |
|---|---|
| Order ID | Unique order identifier |
| Order Date | Date the order was placed |
| Ship Date | Date the order was shipped |
| Customer ID | Unique customer identifier |
| Customer Name | Customer name |
| Segment | Customer segment |
| Region | Sales region |
| Category | Product category |
| Sub-Category | Product sub-category |
| Product Name | Product description |
| Sales | Sales amount |
| Quantity | Number of units sold |
| Discount | Discount applied |
| Profit | Profit or loss generated |

**Dataset dimensions:**
- Orders: 9,994 records
- Returns: 296 records
- People: 4 records
- Analysis period: January 2014 – December 2017

## Technology Stack

| Tool / Technology | Purpose |
|---|---|
| Python | Data processing and analysis |
| Google Colab | Python development environment |
| Pandas | Data manipulation and cleaning |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Exploratory data visualization |
| Microsoft Power BI | Interactive dashboard development |
| DAX | KPI and measure calculations |
| Git & GitHub | Version control and project collaboration |

## Project Workflow

1. **Data Understanding:** Examined the Orders, Returns, and People datasets.
2. **Data Cleaning:** Standardized column names and text values, converted data types, handled missing values, and prepared the return indicator.
3. **Data Integration:** Combined return information with order records.
4. **Feature Engineering:** Created Year, Month, Month Name, Quarter, and YearMonth features.
5. **KPI Calculation:** Calculated sales, profit, orders, customers, average order value, and profit margin.
6. **Exploratory Data Analysis:** Investigated category, product, regional, customer-segment, discount, and time-based performance.
7. **Dashboard Development:** Built interactive visualizations in Power BI.
8. **Business Recommendations:** Identified performance patterns and potential areas for improvement.

## Key Performance Indicators

The following KPIs were calculated from the cleaned dataset:

| KPI | Value |
|---|---:|
| Total Sales | $2,297,200.86 |
| Total Profit | $286,397.02 |
| Total Orders | 5,009 |
| Total Customers | 793 |
| Average Order Value | $458.61 |
| Profit Margin | 12.47% |
| Total Quantity Sold | 37,873 |

**KPI Definitions:**

- **Total Sales:** Sum of all sales transactions.
- **Total Profit:** Sum of profit generated across transactions.
- **Total Orders:** Count of distinct Order IDs.
- **Total Customers:** Count of distinct Customer IDs.
- **Average Order Value:** Total Sales divided by Total Orders.
- **Profit Margin:** Total Profit divided by Total Sales.

## Exploratory Data Analysis — Key Findings

### 1. Category Performance

- Technology generated the highest sales and profit.
- Office Supplies recorded the highest quantity sold.
- Furniture had a relatively low profit margin compared with the other categories.

### 2. Regional Performance

- West recorded the highest sales and profit.
- East was the second-largest contributor to sales.
- Central had the lowest profit margin among the four regions.

### 3. Customer Segment Analysis

- Consumer contributed the highest total sales and profit.
- Home Office recorded the highest profit margin among the three customer segments.
- Corporate and Home Office had higher average order values than Consumer.

### 4. Time-Based Analysis

- Sales increased significantly in 2016 and 2017.
- 2017 recorded the highest annual sales and profit.
- November 2017 recorded the highest monthly sales in the dataset.

### 5. Discount and Profitability Analysis

- Higher discount levels were associated with lower profitability in several product categories.
- Some high-discount transactions generated negative profit.
- Discount strategies should be evaluated alongside product category and profit margin.

*Note: These findings describe patterns in the dataset and do not establish causal relationships.*

## Power BI Dashboard

The dashboard is being developed with the following planned pages:

| Dashboard Page | Focus |
|---|---|
| Executive Overview | Overall business performance and KPIs |
| Product Performance | Category, sub-category, and product analysis |
| Time Trends | Monthly and yearly sales and profit trends |
| Regional & Customer Analysis | Regional and customer-segment performance |

The Executive Overview page currently includes KPI cards, a monthly sales trend, and a yearly sales and profit comparison.

Additional dashboard pages and interactive filtering are part of the ongoing development.

## Repository Structure

The repository currently includes the initial KPI analysis files. Additional project outputs will be organized as development progresses.

```text
project-3-sales-business-performance-analytics/
│
├── Dataset/
│   ├── Sample - Superstore.xlsm
│   └── superstore_powerbi.csv
│
├── EDA/
│   ├── figures/
│   │   ├── category_discount_impact.png
│   │   ├── category_sales_profit_performance.png
│   │   ├── customer_segment_performance.png
│   │   ├── discount_impact_on_profit_margin.png
│   │   ├── monthly_sales_profit_trend.png
│   │   ├── regional_sales_profit_performance.png
│   │   ├── top_10_products_by_profit.png
│   │   ├── top_10_products_by_sales.png
│   │   └── yearly_sales_profit_performance.png
│   │
│   ├── notebooks/
│   │   └── Sales_Business_Performance_Analysis.ipynb
│   │
│   └── outputs/
│       ├── category_discount_analysis.csv
│       ├── category_summary.csv
│       ├── discount_summary.csv
│       ├── monthly_sales.csv
│       ├── region_summary.csv
│       ├── segment_summary.csv
│       ├── top_products_by_profit.csv
│       ├── top_products_by_sales.csv
│       └── yearly_summary.csv
│
└── README.md
```

The cleaned datasets, EDA outputs, Power BI dashboard, and final analytical report can be added to the repository as they are finalized.

## Business Recommendations

Based on the exploratory analysis:

1. **Improve Furniture Profitability:** Review pricing, operational costs, and discount policies for the Furniture category.
2. **Optimize Discount Strategies:** Evaluate high-discount transactions carefully to reduce potential losses.
3. **Leverage Technology Performance:** Identify successful Technology products and explore opportunities to expand their contribution.
4. **Investigate Regional Differences:** Analyze the Central region's relatively low profit margin and identify improvement opportunities.
5. **Strengthen Customer Retention:** Use segment-level purchasing patterns to develop targeted customer strategies.

## Project Status

<details>
<summary>Development progress</summary>

- [x] Dataset exploration
- [x] Data cleaning and preprocessing
- [x] KPI calculation
- [x] Exploratory data analysis
- [x] EDA charts and summary files
- [x] Power BI data preparation
- [x] Executive Overview dashboard page
- [ ] Product Performance dashboard page
- [ ] Time Trends dashboard page
- [ ] Regional & Customer Analysis dashboard page
- [ ] Final dashboard validation
- [ ] Final analytical report and recommendations

</details>

## Contributors

This is a collaborative academic project.

- Jinal Sasiya
- Anvi Gupta
- Mohd Faizan Usmani
- Dasari Adithya
- Sarthak Raina
## Conclusion

This project demonstrates how data analytics and business intelligence tools can be used to extract meaningful insights from transactional retail data. By combining Python-based analysis with Power BI visualizations, the project aims to provide a comprehensive view of business performance and support informed decision-making.

---

**Project:** Sales & Business Performance Analytics Dashboard  
**Dataset:** Sample Superstore  
**Tools:** Python, Google Colab, Microsoft Power BI, DAX, GitHub
