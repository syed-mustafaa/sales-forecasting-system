# Business Context: Sales Forecasting & Inventory Optimization

## 1. Problem Statement
**"TechTrend Retail"**, a mid-sized electronics retailer, is facing significant operational inefficiencies.
- **Stockouts**: High-demand products (e.g., latest smartphones, gaming consoles) frequently run out of stock, leading to lost revenue and customer dissatisfaction.
- **Overstock**: Low-demand accessories and older models are piling up in warehouses, tying up working capital and incurring storage costs.
- **Reactive Ordering**: Reordering is currently done manually based on "gut feeling" rather than data-driven forecasts.

**Goal**: Build an automated end-to-end system to forecast sales demand and generate optimized inventory restocking recommendations.

## 2. Key Performance Indicators (KPIs)
We will measure success using the following metrics:

### A. Operational Metrics
1.  **Stockout Rate (%)**: Percentage of days a product has zero inventory.
    *   `Formula: (Days with 0 Stock / Total Days) * 100`
2.  **Inventory Turnover Ratio**: How often inventory is sold and replaced over a period.
    *   `Formula: Cost of Goods Sold (COGS) / Average Inventory Value`
3.  **Days Sales of Inventory (DSI)**: Average number of days it takes to sell inventory.
    *   `Formula: (Average Inventory / COGS) * 365`

### B. Forecasting Metrics
4.  **Forecast Accuracy**: The complement of error.
    *   `Formula: 1 - MAPE (Mean Absolute Percentage Error)`
5.  **Bias**: Tendency to consistently over-forecast or under-forecast.

## 3. Business Questions to Answer
1.  **What to Order?**: Which SKUs are approaching their reorder point?
2.  **How Much to Order?**: What is the optimal quantity to minimize cost (EOQ) while maintaining service levels?
3.  **When to Order?**: Based on supplier lead times, when should the PO be placed?
4.  **Seasonal Trends**: How much extra stock is needed for Black Friday / Christmas?

## 4. Terminology
- **SKU**: Stock Keeping Unit (unique product identifier).
- **Lead Time**: Time between placing an order and receiving it.
- **Safety Stock**: Buffer stock to protect against demand variability and lead time delays.
- **Reorder Point (ROP)**: Inventory level at which a new order should be placed.
    *   `Formula: (Avg Daily Usage * Avg Lead Time) + Safety Stock`
- **EOQ**: Economic Order Quantity, the ideal order quantity a company should purchase.
