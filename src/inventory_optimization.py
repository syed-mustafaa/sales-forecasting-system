import pandas as pd
import numpy as np
import os

# Create directory for output
os.makedirs("data/optimization", exist_ok=True)

def load_data():
    master_table = pd.read_csv("data/processed/master_table.csv", parse_dates=['date'])
    products = pd.read_csv("data/raw/products.csv")
    suppliers = pd.read_csv("data/raw/suppliers.csv")
    
    # Merge supplier info to products if not already there
    if 'lead_time_days' not in products.columns:
        products = products.merge(suppliers[['supplier_id', 'lead_time_days']], on='supplier_id', how='left')
        
    return master_table, products

def calculate_inventory_metrics(master_table, products):
    # 1. Calculate Average Daily Sales (ADS) and Standard Deviation (for Safety Stock)
    # We'll use the last 90 days for recent demand trends
    recent_period = master_table[master_table['date'] > master_table['date'].max() - pd.Timedelta(days=90)]
    
    product_metrics = recent_period.groupby('product_id').agg(
        avg_daily_sales=('quantity', 'mean'),
        std_daily_sales=('quantity', 'std')
    ).reset_index()
    
    # Merge with product details (cost, lead time)
    product_metrics = product_metrics.merge(products, on='product_id', how='left')
    
    # 2. Safety Stock (SS)
    # Formula: Z-score * StdDev(Demand) * Sqrt(Lead Time)
    # Assuming 95% Service Level -> Z = 1.65
    Z_SCORE = 1.65
    
    product_metrics['safety_stock'] = Z_SCORE * product_metrics['std_daily_sales'] * np.sqrt(product_metrics['lead_time_days'])
    product_metrics['safety_stock'] = product_metrics['safety_stock'].apply(np.ceil)
    
    # 3. Reorder Point (ROP)
    # Formula: (Avg Daily Sales * Lead Time) + Safety Stock
    product_metrics['reorder_point'] = (product_metrics['avg_daily_sales'] * product_metrics['lead_time_days']) + product_metrics['safety_stock']
    product_metrics['reorder_point'] = product_metrics['reorder_point'].apply(np.ceil)
    
    # 4. Economic Order Quantity (EOQ)
    # Formula: Sqrt( (2 * Demand * Order Cost) / Holding Cost )
    # Assumptions:
    # - Annual Demand = Avg Daily Sales * 365
    # - Order Cost (Fixed cost per order) = $50 (assumption)
    # - Holding Cost = 20% of Unit Cost per year (assumption)
    
    ORDER_COST = 50.0
    HOLDING_COST_PCT = 0.20
    
    product_metrics['annual_demand'] = product_metrics['avg_daily_sales'] * 365
    product_metrics['holding_cost_per_unit'] = product_metrics['cost_price'] * HOLDING_COST_PCT
    
    product_metrics['eoq'] = np.sqrt(
        (2 * product_metrics['annual_demand'] * ORDER_COST) / product_metrics['holding_cost_per_unit']
    )
    product_metrics['eoq'] = product_metrics['eoq'].apply(np.ceil)
    
    return product_metrics

def identify_risks(master_table, product_metrics):
    # Get latest stock levels
    latest_date = master_table['date'].max()
    current_stock = master_table[master_table['date'] == latest_date][['product_id', 'stock_on_hand']]
    
    # Merge with calculated metrics
    risk_analysis = current_stock.merge(product_metrics, on='product_id', how='left')
    
    # Detect Risks
    # Risk: Low Stock (Current Stock <= ROP)
    risk_analysis['risk_status'] = 'Healthy'
    risk_analysis.loc[risk_analysis['stock_on_hand'] <= risk_analysis['reorder_point'], 'risk_status'] = 'Low Stock - Reorder Now'
    
    # Risk: Overstock (Current Stock > 3 * ROP - arbitrary threshold for demo)
    # Or based on Days Sales of Inventory (DSI) > 60 days
    risk_analysis['dsi'] = risk_analysis['stock_on_hand'] / risk_analysis['avg_daily_sales']
    risk_analysis.loc[(risk_analysis['risk_status'] == 'Healthy') & (risk_analysis['dsi'] > 90), 'risk_status'] = 'Overstock - Reduce'
    
    return risk_analysis

if __name__ == "__main__":
    print("Loading data for Optimization...")
    master_table, products = load_data()
    
    print("Calculating ROP, Safety Stock, EOQ...")
    product_metrics = calculate_inventory_metrics(master_table, products)
    
    print("Identifying Inventory Risks...")
    risk_analysis = identify_risks(master_table, product_metrics)
    
    # Prepare final recommendation table
    recommendations = risk_analysis[[
        'product_id', 'product_name', 'category', 'stock_on_hand', 
        'reorder_point', 'safety_stock', 'eoq', 'risk_status'
    ]]
    
    print(f"Recommendations generated for {len(recommendations)} products.")
    print(recommendations['risk_status'].value_counts())
    
    output_path = "data/optimization/inventory_recommendations.csv"
    recommendations.to_csv(output_path, index=False)
    print(f"Saved recommendations to {output_path}")
