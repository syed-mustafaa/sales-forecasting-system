# Sales Forecasting & Inventory Optimization System

## 📊 Project Overview
This project is an end-to-end data analytics solution designed to optimize inventory management for a retail business ("TechTrend Retail"). It leverages historical sales data to forecast future demand and generate automated restocking recommendations, aiming to reduce stockouts and minimize excess inventory costs.

## 🚀 Key Features
- **Synthetic Data Generation**: Creates realistic retail datasets (Sales, Inventory, Products, Suppliers) with seasonal trends and patterns.
- **Data Analytics**: Comprehensive Exploratory Data Analysis (EDA) to identify top products and sales trends.
- **Demand Forecasting**: Uses Exponential Smoothing (Holt-Winters) to predict sales for the next 30 days.
- **Inventory Optimization**: Calculates Safety Stock, Reorder Points (ROP), and Economic Order Quantity (EOQ).
- **Interactive Dashboard**: A Streamlit-based dashboard for visualizing business metrics and inventory risks.

## 📂 Project Structure
```
sales_forecasting_system/
├── data/
│   ├── raw/            # Generated synthetic data
│   ├── processed/      # Cleaned master tables
│   ├── predictions/    # Forecast outputs
│   └── optimization/   # Inventory recommendations
├── reports/
│   └── figures/        # EDA visualizations
├── src/
│   ├── data_generation.py      # Generates synthetic data
│   ├── data_cleaning.py        # Cleans and merges data
│   ├── eda_analysis.py         # Performs EDA and plots figures
│   ├── forecasting.py          # Runs forecasting models
│   ├── inventory_optimization.py # Calculates ROP, EOQ
│   └── dashboard.py            # Streamlit dashboard app
├── business_context.md         # Problem statement and KPIs
├── FINAL_REPORT.md             # Executive summary of findings
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## 🛠️ Setup & Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/syed-mustafaa/sales-forecasting-system.git
    cd sales-forecasting-system
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ How to Run

1.  **Generate Data** (Optional, if starting fresh)
    ```bash
    python src/data_generation.py
    ```

2.  **Run Data Pipeline**
    Process data, run analysis, forecast, and optimize:
    ```bash
    python src/data_cleaning.py
    python src/eda_analysis.py
    python src/forecasting.py
    python src/inventory_optimization.py
    ```

3.  **Launch Dashboard**
    View the interactive insights:
    ```bash
    streamlit run src/dashboard.py
    ```

## 📈 Results
- **Forecast Accuracy**: The model achieved a MAPE of **~24%** on test data.
- **Inventory Risk**: Identified 27 products requiring immediate restocking.
- See `FINAL_REPORT.md` for a detailed analysis of findings.
