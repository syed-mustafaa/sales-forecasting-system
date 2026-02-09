import pandas as pd
import numpy as np
import os

# Paths
RAW_DATA_PATH = "data/raw"
PROCESSED_DATA_PATH = "data/processed"
os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

def load_data():
    print("Loading data...")
    sales = pd.read_csv(f"{RAW_DATA_PATH}/sales.csv")
    inventory = pd.read_csv(f"{RAW_DATA_PATH}/inventory.csv")
    products = pd.read_csv(f"{RAW_DATA_PATH}/products.csv")
    suppliers = pd.read_csv(f"{RAW_DATA_PATH}/suppliers.csv")
    return sales, inventory, products, suppliers

def clean_data(sales, inventory, products, suppliers):
    print("Cleaning and merging data...")
    
    # Date conversion
    sales['date'] = pd.to_datetime(sales['date'])
    inventory['date'] = pd.to_datetime(inventory['date'])
    
    # Merge Sales with Product Info
    sales_merged = sales.merge(products, on='product_id', how='left')
    
    # Merge with Supplier Info
    sales_merged = sales_merged.merge(suppliers, on='supplier_id', how='left')
    
    # Feature Engineering
    sales_merged['year'] = sales_merged['date'].dt.year
    sales_merged['month'] = sales_merged['date'].dt.month
    sales_merged['week'] = sales_merged['date'].dt.isocalendar().week
    sales_merged['day_of_week'] = sales_merged['date'].dt.dayofweek
    sales_merged['is_weekend'] = sales_merged['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    
    sales_merged['revenue'] = sales_merged['quantity'] * sales_merged['selling_price']
    sales_merged['profit'] = sales_merged['revenue'] - (sales_merged['quantity'] * sales_merged['cost_price'])
    
    # Sort by date
    sales_merged = sales_merged.sort_values(by='date').reset_index(drop=True)
    
    return sales_merged

def aggregate_data(sales_merged):
    print("Creating daily aggregations...")
    # Daily Sales per Product
    daily_sales = sales_merged.groupby(['date', 'product_id']).agg({
        'quantity': 'sum',
        'revenue': 'sum',
        'profit': 'sum'
    }).reset_index()
    
    return daily_sales

if __name__ == "__main__":
    sales, inventory, products, suppliers = load_data()
    
    # Clean Sales Data
    cleaned_sales = clean_data(sales, inventory, products, suppliers)
    
    # Save cleaned transaction data
    cleaned_sales.to_csv(f"{PROCESSED_DATA_PATH}/sales_cleaned.csv", index=False)
    
    # Aggregate to Daily Level (Master Table for Forecasting)
    daily_sales = aggregate_data(cleaned_sales)
    
    # Merge Daily Sales with Inventory Snapshot
    # Note: Inventory snapshot is daily, so we can merge directly
    inventory['date'] = pd.to_datetime(inventory['date'])
    master_table = daily_sales.merge(inventory, on=['date', 'product_id'], how='outer')
    
    # Fill missing values for sales (days with no sales = 0 sales)
    # Be careful: No sales could mean no demand OR stockout. 
    # For now, we fill sales with 0, but we will deal with stockouts in analysis.
    master_table['quantity'].fillna(0, inplace=True)
    master_table['revenue'].fillna(0, inplace=True)
    master_table['profit'].fillna(0, inplace=True)
    
    # Fill missing stock (if any) with 0? Or ffill?
    # Assuming inventory snapshot is comprehensive, missing means 0 or missing data.
    # Let's assume 0 stock for now if missing in inventory table but present in sales (rare)
    master_table['stock_on_hand'].fillna(0, inplace=True) 

    # Re-merge product details to master table
    master_table = master_table.merge(products, on='product_id', how='left')
    
    print(f"Master Table Shape: {master_table.shape}")
    master_table.to_csv(f"{PROCESSED_DATA_PATH}/master_table.csv", index=False)
    
    print("Data cleaning complete! Files saved in data/processed/")
