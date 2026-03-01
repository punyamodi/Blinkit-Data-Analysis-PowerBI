# Blinkit Sales Analytics

An end-to-end interactive sales analytics dashboard built with Python and Streamlit, analysing Blinkit grocery data across outlets, product categories, and customer ratings.

![Dashboard](https://github.com/user-attachments/assets/26f3cb56-a38f-4fde-bfdf-4defc771faeb)

## Overview

The dashboard provides real-time filtering and visualisation of 8,523 grocery transactions sourced from Blinkit outlets spanning 2011 to 2022. All charts are interactive and respond to the sidebar filter panel.

## Features

**KPI Cards**
- Total Sales, Average Sales per Transaction, Items Sold, Average Customer Rating

**Sales Analysis**
- Sales breakdown by fat content (Regular vs Low Fat)
- Sales by item type across 16 product categories
- Fat content sales segmented by location tier
- Top 10 highest-grossing items

**Outlet Analysis**
- Sales by outlet size (Small, Medium, High)
- Sales by location tier (Tier 1, 2, 3)
- Outlet establishment trend over time with area chart
- Sales performance by outlet age band
- Full outlet type comparison table (Total Sales, Item Count, Avg Sales, Avg Rating, Avg Visibility)

**Filters**
- Location tier, outlet size, item type, fat content, outlet type, establishment year range

**Export**
- Download the current filtered dataset as a CSV file

## Project Structure

```
.
├── app.py                  # Streamlit dashboard entry point
├── src/
│   ├── pipeline.py         # Data loading, cleaning, and transformation
│   ├── metrics.py          # Aggregation and KPI computation functions
│   └── charts.py           # Plotly chart builders
├── data/
│   └── blinkit_grocery_data.xlsx
└── requirements.txt
```

## Setup

**Requirements:** Python 3.10+

```bash
git clone https://github.com/<your-username>/Blinkit-Data-Analysis-PowerBI.git
cd Blinkit-Data-Analysis-PowerBI
pip install -r requirements.txt
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`.

## Data Pipeline

The pipeline (`src/pipeline.py`) performs the following transformations on the raw Excel data:

1. **Column normalisation** — renames all columns to snake_case
2. **Fat content standardisation** — maps `LF`, `low fat`, `reg` to canonical `Low Fat` / `Regular`
3. **Weight imputation** — fills missing item weights with the per-category mean
4. **Visibility correction** — replaces zero-visibility entries with the per-category mean
5. **Outlet age derivation** — computes `outlet_age = 2024 - outlet_establishment_year`

## Key Insights

| Insight | Detail |
|---|---|
| Total revenue | $1.20M across all outlets |
| Top product category | Fruits and Vegetables |
| Consumer preference | Low-fat products outperform Regular in Tier 3 |
| Best outlet size | Medium outlets generate the highest total sales |
| Best location tier | Tier 3 outlets lead in total revenue |
| Rating average | 3.97 out of 5 across all transactions |

## Tech Stack

| Layer | Library |
|---|---|
| Data processing | pandas, numpy |
| Visualisation | Plotly |
| Dashboard | Streamlit |
| Data source | openpyxl (Excel) |

## License

This project is released for educational and portfolio purposes. The underlying dataset is used solely for demonstration.
