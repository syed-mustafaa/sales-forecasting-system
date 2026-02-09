import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create directories for reports
os.makedirs("reports/figures", exist_ok=True)

def load_processed_data():
    return pd.read_csv("data/processed/master_table.csv", parse_dates=['date'])

def plot_sales_trends(df):
    plt.figure(figsize=(12, 6))
    daily_sales = df.groupby('date')['revenue'].sum()
    daily_sales.plot()
    plt.title('Total Daily Sales Revenue')
    plt.ylabel('Revenue ($)')
    plt.xlabel('Date')
    plt.savefig('reports/figures/daily_sales_trend.png')
    plt.close()
    
    # Weekly Trend
    plt.figure(figsize=(12, 6))
    weekly_sales = df.set_index('date').resample('W')['revenue'].sum()
    weekly_sales.plot(kind='bar')
    plt.title('Weekly Sales Revenue')
    plt.ylabel('Revenue ($)')
    plt.xlabel('Week')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('reports/figures/weekly_sales_trend.png')
    plt.close()

def plot_top_products(df):
    try:
        top_products = df.groupby('product_name')['revenue'].sum().sort_values(ascending=False).head(10)
        
        plt.figure(figsize=(10, 6))
        # Use simple pandas plotting to avoid seaborn complexity for now
        top_products.sort_values().plot(kind='barh', color='skyblue')
        plt.title('Top 10 Products by Revenue')
        plt.xlabel('Total Revenue ($)')
        plt.tight_layout()
        plt.savefig('reports/figures/top_10_products.png')
        plt.close()
    except Exception as e:
        print(f"Error plotting top products: {e}")

def plot_seasonality(df):
    try:
        plt.figure(figsize=(10, 6))
        # Use pandas boxplot or seaborn
        sns.boxplot(data=df, x='month', y='revenue')
        plt.title('Monthly Sales Distribution (Seasonality)')
        plt.xlabel('Month')
        plt.ylabel('Revenue')
        plt.savefig('reports/figures/monthly_seasonality.png')
        plt.close()
    except Exception as e:
        print(f"Error plotting seasonality: {e}")

if __name__ == "__main__":
    print("Loading data for EDA...")
    df = load_processed_data()
    
    print("Generating Sales Trend Plots...")
    plot_sales_trends(df)
    
    print("Generating Top Products Plot...")
    plot_top_products(df)
    
    print("Generating Seasonality Plot...")
    plot_seasonality(df)
    
    print("EDA Visualizations saved to reports/figures/")
