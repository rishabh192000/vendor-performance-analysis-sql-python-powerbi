# Vendor Performance Analysis – Retail Inventory & Sales

Analyzing vendor efficiency and profitability to support strategic purchasing and inventory decisions using **SQL, Python, and Power BI**.

---

## 📚 Table of Contents

- [Overview](#overview)
- [Business Problem](#business-problem)
- [Dataset](#dataset)
- [Tools & Technologies](#tools--technologies)
- [Project Structure](#project-structure)
- [Data Cleaning & Preparation](#data-cleaning--preparation)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
- [Research Questions & Key Findings](#research-questions--key-findings)
- [Power BI Dashboard](#power-bi-dashboard)
- [How to Run This Project](#how-to-run-this-project)
- [Results & Recommendations](#results--recommendations)
- [Future Work](#future-work)
- [Author & Contact](#author--contact)

---

## Overview

This end-to-end **data analytics project** evaluates vendor performance in a retail and wholesale environment to improve pricing strategy, purchasing decisions, and inventory efficiency.

---

## Business Problem

Retail businesses rely heavily on vendors for revenue and inventory movement. Poor pricing, inefficient turnover, or weak vendor partnerships can significantly reduce profitability.

This project answers:
1. Which vendors contribute most to sales and profit?
2. Which brands are underperforming?
3. How efficiently is inventory converted into sales?
4. Are profit margins statistically different across vendors?
5. Which vendors should be prioritized or reconsidered?

---

## Dataset

- Source: Simulated real-world retail data
- Location: `data/`
- Period: One year

Raw tables:
- purchases.csv
- purchase_prices.csv
- sales.csv
- vendor_invoice.csv
- begin_inventory.csv
- end_inventory.csv

---

## Tools & Technologies

- **SQL** (SQLite, joins, aggregations)
- **Python** (pandas, NumPy, Matplotlib, Seaborn, SciPy)
- **Power BI** (interactive dashboards, DAX)
- **Git & GitHub**
- **Markdown**

---

## Project Structure

```
vendor-performance-analysis/
├── README.md
├── .gitignore
├── requirements.txt
├── Vendor Performance Report.pdf
├── notebooks/
│   ├── exploratory_data_analysis.ipynb
│   └── vendor_performance_analysis.ipynb
├── scripts/
│   ├── ingestion_db.py
│   └── get_vendor_summary.py
└── dashboard/
    └── vendor_performance_dashboard.pbix
```

## Data Cleaning & Preparation

- Loaded CSV files into SQLite using a structured ETL pipeline  
- Removed invalid records (zero prices, duplicates)  
- Standardized numeric and text fields  
- Treated missing sales values as unsold inventory  
- Created metrics:
  - Gross Profit
  - Profit Margin
  - Stock Turnover

---

## Exploratory Data Analysis (EDA)

- Distribution analysis of sales, profit, and margins  
- Sales vs margin trade-off analysis  
- Inventory turnover comparison  
- Vendor and brand-level summaries  

**Key insight:**  
> High-margin vendors are not always high-volume sellers.

---

## Research Questions & Key Findings

- A small number of vendors drive most profit  
- Profit margin differences are statistically significant (p < 0.05)  
- High-margin, low-sales brands are promotion candidates  
- Low-margin, high-sales brands need pricing review  
### RQ1: Who are the top and bottom vendors?

- A small subset of vendors contributes a majority of gross profit.
- Bottom vendors add minimal value and often have low margins and poor turnover.

### RQ2: Is there a significant difference in profit margins between top and low performers?

- Two-sample t-test on profit margins between top and bottom sales quartiles.
- Result: p-value ≪ 0.05 → **Statistically significant difference**.
- Conclusion: performance differences are real and can guide vendor strategy.

### RQ3: Which brands need pricing or promotional adjustments?

- High-margin, low-sales brands identified as **promotion candidates**.
- High-sales, low-margin brands flagged for **pricing/negotiation review**.

### RQ4: How efficient is inventory usage?

- Stock turnover varies widely across vendors.
- Vendors with low turnover tie up working capital and may need inventory rationalization.
---

## Power BI Dashboard

![Power BI Dashboard](images/dashboard_image.png)


Dashboard includes:
- KPI cards  
- Top vendors by sales and profit  
- Profit vs sales scatter plot  
- Interactive slicers  

---

## How to Run This Project

1. Clone the repo  
   ```bash
   git clone https://github.com/your-username/vendor-performance-analysis.git

2. Load the CSV files and ingest data into the database:
    ```bash
    python scripts/ingestion_db.py

3. Create the vendor summary table:
    ```bash
    python scripts/get_vendor_summary.py


4. Open and run the Jupyter notebooks:
    ```bash
    notebooks/exploratory_data_analysis.ipynb
    notebooks/vendor_performance_analysis.ipynb

5. Open the Power BI dashboard:
    dashboard/vendor_performance_dashboard.pbix


## Results & Recommendations

- Strengthen partnerships with high-performing vendors
- Promote high-margin, low-volume brands
- Reduce slow-moving inventory
- Optimize pricing strategies

## Future Work 
- Demand forecasting
- Automated ETL
- Vendor scoring model
- Power BI Service deployment

## Author & Contact

**Rishabh Verma**
[Email] (rishabhv01920@gmail.com)
[LinkedIn] (https://www.linkedin.com/in/rishabh-verma-4b9611224/)
