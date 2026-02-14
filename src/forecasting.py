import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import os

# Create directories for reports
os.makedirs("data/predictions", exist_ok=True)
os.makedirs("reports/figures", exist_ok=True)

def load_data():
    df = pd.read_csv("data/processed/master_table.csv", parse_dates=['date'])
    # Aggregate to total daily sales for simplicity in this demo
    daily_sales = df.groupby('date')['revenue'].sum().reset_index()
    daily_sales = daily_sales.set_index('date').asfreq('D').fillna(0)
    return daily_sales

def train_prophet(df):
    # Optional: Implement Prophet if libraries allow. 
    # For now, sticking to statsmodels for robustness.
    pass

def train_exponential_smoothing(train_data, test_data, horizon):
    # Triple Exponential Smoothing (Holt-Winters)
    # Additive trend, Additive seasonality (assuming 7-day or yearly?)
    # Valid seasons: 7 (weekly)
    
    model = ExponentialSmoothing(
        train_data['revenue'],
        trend='add',
        seasonal='add',
        seasonal_periods=7
    ).fit()
    
    forecast = model.forecast(steps=len(test_data))
    future_forecast = model.forecast(steps=len(test_data) + horizon)
    
    return forecast, future_forecast, model

def evaluate_model(actual, forecast, model_name):
    mape = mean_absolute_percentage_error(actual, forecast)
    rmse = np.sqrt(mean_squared_error(actual, forecast))
    print(f"Model: {model_name} | MAPE: {mape:.2%} | RMSE: {rmse:.2f}")
    return mape, rmse

if __name__ == "__main__":
    print("-" * 50)
    print("Starting Sales Forecasting Pipeline...")
    print("-" * 50)
    print("Loading data...")
    df = load_data()
    
    # Split Train/Test (Last 30 days for testing)
    test_days = 30
    train_data = df.iloc[:-test_days]
    test_data = df.iloc[-test_days:]
    
    print(f"Training Range: {train_data.index.min()} to {train_data.index.max()}")
    print(f"Testing Range: {test_data.index.min()} to {test_data.index.max()}")
    
    # Train Model
    print("Training Exponential Smoothing Model...")
    forecast_test, forecast_future, model = train_exponential_smoothing(train_data, test_data, horizon=30)
    
    # Evaluate
    evaluate_model(test_data['revenue'], forecast_test, "Exponential Smoothing")
    
    # Plot Forecasting
    plt.figure(figsize=(14, 7))
    plt.plot(train_data.index, train_data['revenue'], label='Train Data')
    plt.plot(test_data.index, test_data['revenue'], label='Actual Test Data', color='green')
    plt.plot(test_data.index, forecast_test, label='Forecast (Test)', color='red', linestyle='--')
    # Plot future
    future_dates = pd.date_range(start=test_data.index.max() + pd.Timedelta(days=1), periods=30)
    # The 'forecast_future' above includes the test period in statsmodels logic often, 
    # but forecast() returns exactly 'steps' ahead from end of training.
    # So `forecast_future` called with steps=60 (test+30) would cover both.
    # Let's simplify: forecast from END of ALL data.
    
    # Re-train on ALL data for final forecast
    final_model = ExponentialSmoothing(
        df['revenue'],
        trend='add',
        seasonal='add',
        seasonal_periods=7
    ).fit()
    final_forecast_30 = final_model.forecast(steps=30)
    
    plt.plot(future_dates, final_forecast_30, label='Future Forecast (30 Days)', color='orange')
    
    plt.title('Sales Forecast: Exponential Smoothing')
    plt.legend()
    plt.savefig('reports/figures/forecast_30days.png')
    plt.close()
    
    # Save Forecasts
    forecast_df = pd.DataFrame({
        'date': future_dates,
        'forecasted_revenue': final_forecast_30
    })
    forecast_df.to_csv("data/predictions/forecast_30days.csv", index=False)
    
    print("Forecasting complete. Results saved.")
