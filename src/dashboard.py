import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Page Config
st.set_page_config(page_title="Retail Forecasting Dashboard", layout="wide")

@st.cache_data
def load_data():
    master_table = pd.read_csv("data/processed/master_table.csv", parse_dates=['date'])
    forecasts = pd.read_csv("data/predictions/forecast_30days.csv", parse_dates=['date'])
    recommendations = pd.read_csv("data/optimization/inventory_recommendations.csv")
    return master_table, forecasts, recommendations

try:
    master_table, forecasts, recommendations = load_data()
except FileNotFoundError:
    st.error("Data files not found. Please run the data pipeline first.")
    st.stop()

# Sidebar
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Sales Analytics", "Forecast", "Inventory Optimization"])

if page == "Overview":
    st.title("📊 Retail Business Overview")
    
    # Key Metrics
    total_revenue = master_table['revenue'].sum()
    total_profit = master_table['profit'].sum()
    total_sales_qty = master_table['quantity'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Units Sold", f"{total_sales_qty:,}")
    
    # Recent Trend
    st.subheader("Recent Sales Trend (Last 30 Days)")
    recent_sales = master_table.groupby('date')['revenue'].sum().tail(30).reset_index()
    fig = px.line(recent_sales, x='date', y='revenue', title="Daily Revenue")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Sales Analytics":
    st.title("📈 Sales Analytics")
    
    # Top Products
    top_products = master_table.groupby('product_name')['revenue'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_top = px.bar(top_products, x='revenue', y='product_name', orientation='h', title="Top 10 Products by Revenue")
    st.plotly_chart(fig_top, use_container_width=True)
    
    # Category Performance
    cat_perf = master_table.groupby('category')['revenue'].sum().reset_index()
    fig_cat = px.pie(cat_perf, values='revenue', names='category', title="Revenue by Category")
    st.plotly_chart(fig_cat, use_container_width=True)

elif page == "Forecast":
    st.title("🔮 Demand Forecast (Next 30 Days)")
    
    # Historical + Forecast
    historical = master_table.groupby('date')['revenue'].sum().reset_index()
    historical['Type'] = 'Historical'
    
    forecast_plot = forecasts.copy()
    forecast_plot.columns = ['date', 'revenue']
    forecast_plot['Type'] = 'Forecast'
    
    combined = pd.concat([historical.tail(90), forecast_plot])
    
    fig = px.line(combined, x='date', y='revenue', color='Type', title="Sales Forecast")
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(forecasts.head(10))

elif page == "Inventory Optimization":
    st.title("📦 Inventory Optimization")
    
    # Risk Summary
    risk_counts = recommendations['risk_status'].value_counts().reset_index()
    risk_counts.columns = ['Status', 'Count']
    fig_risk = px.pie(risk_counts, values='Count', names='Status', title="Inventory Risk Distribution", color='Status',
                      color_discrete_map={'Healthy': 'green', 'Low Stock - Reorder Now': 'red', 'Overstock - Reduce': 'orange'})
    st.plotly_chart(fig_risk, use_container_width=True)
    
    # Reorder Recommendations
    st.subheader("🔴 Low Stock Alerts - Reorder Immediately")
    reorder_list = recommendations[recommendations['risk_status'] == 'Low Stock - Reorder Now']
    st.dataframe(reorder_list[['product_name', 'category', 'stock_on_hand', 'reorder_point', 'eoq']])
    
    st.subheader("🟠 Overstock Alerts - Run Promotions")
    overstock_list = recommendations[recommendations['risk_status'] == 'Overstock - Reduce']
    st.dataframe(overstock_list[['product_name', 'category', 'stock_on_hand', 'avg_daily_sales']])

st.sidebar.info("Built with Streamlit & Python")
