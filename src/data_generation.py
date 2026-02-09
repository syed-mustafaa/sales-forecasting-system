import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Initialize Faker
fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Configuration
NUM_PRODUCTS = 50
NUM_SUPPLIERS = 10
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2023, 12, 31)
DAYS = (END_DATE - START_DATE).days + 1

# Output paths
RAW_DATA_PATH = "data/raw"
os.makedirs(RAW_DATA_PATH, exist_ok=True)

def generate_suppliers(n=10):
    suppliers = []
    for i in range(n):
        suppliers.append({
            "supplier_id": f"SUP_{i+1:03d}",
            "supplier_name": fake.company(),
            "lead_time_days": random.randint(3, 14)  # Lead time varies between 3 to 14 days
        })
    return pd.DataFrame(suppliers)

def generate_products(n=50, supplier_ids=[]):
    categories = ['Electronics', 'Home Appliances', 'Clothing', 'Toys', 'Books']
    products = []
    for i in range(n):
        category = random.choice(categories)
        cost_price = round(random.uniform(10, 500), 2)
        selling_price = round(cost_price * random.uniform(1.2, 2.0), 2)  # 20-100% markup
        
        products.append({
            "product_id": f"PROD_{i+1:04d}",
            "product_name": f"{category} - {fake.word().title()}",
            "category": category,
            "cost_price": cost_price,
            "selling_price": selling_price,
            "supplier_id": random.choice(supplier_ids)
        })
    return pd.DataFrame(products)

def generate_sales(products_df, start_date, days):
    sales_data = []
    product_ids = products_df['product_id'].tolist()
    product_prices = dict(zip(products_df['product_id'], products_df['selling_price']))
    
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        is_weekend = current_date.weekday() >= 5
        
        # Seasonality: Higher sales in Q4 (Oct-Dec)
        month = current_date.month
        seasonality_factor = 1.5 if month >= 10 else 1.0
        
        # Random daily transaction count (higher on weekends)
        num_transactions = random.randint(20, 50)
        if is_weekend:
            num_transactions = int(num_transactions * 1.3)
            
        num_transactions = int(num_transactions * seasonality_factor)
        
        for _ in range(num_transactions):
            product_id = random.choice(product_ids)
            quantity = random.randint(1, 5)
            price = product_prices[product_id] # Assuming no price changes for simplicity
            
            sales_data.append({
                "transaction_id": fake.uuid4(),
                "date": current_date.strftime("%Y-%m-%d"),
                "product_id": product_id,
                "quantity": quantity,
                "total_amount": round(quantity * price, 2)
            })
            
    return pd.DataFrame(sales_data)

def generate_inventory(products_df, start_date, days):
    # This is a simplified inventory snapshot generation
    # Ideally, inventory = prev_inventory - sales + restock
    # Here we simulate random stock levels to detect stockouts/overstock
    
    inventory_data = []
    product_ids = products_df['product_id'].tolist()
    
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        
        for product_id in product_ids:
            # Simulate random stock levels
            # Occasional stockouts (0 stock)
            if random.random() < 0.05:
                stock_on_hand = 0
            else:
                stock_on_hand = random.randint(0, 100)
            
            inventory_data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "product_id": product_id,
                "stock_on_hand": stock_on_hand
            })
            
    return pd.DataFrame(inventory_data)

if __name__ == "__main__":
    print("Generating Suppliers...")
    suppliers_df = generate_suppliers(NUM_SUPPLIERS)
    suppliers_df.to_csv(f"{RAW_DATA_PATH}/suppliers.csv", index=False)
    
    print("Generating Products...")
    products_df = generate_products(NUM_PRODUCTS, suppliers_df['supplier_id'].tolist())
    products_df.to_csv(f"{RAW_DATA_PATH}/products.csv", index=False)
    
    print("Generating Sales Transactions...")
    sales_df = generate_sales(products_df, START_DATE, DAYS)
    sales_df.to_csv(f"{RAW_DATA_PATH}/sales.csv", index=False)
    
    print("Generating Inventory Snapshots...")
    inventory_df = generate_inventory(products_df, START_DATE, DAYS)
    inventory_df.to_csv(f"{RAW_DATA_PATH}/inventory.csv", index=False)
    
    print("Data generation complete! Files saved in data/raw/")
