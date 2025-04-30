import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings

warnings.filterwarnings("ignore")  # Suppress warnings

def show(df):
    st.title("📅 Forecasting Future Reviews")
    
    df["Year-Month"] = df["date"].dt.to_period("M").astype(str)
    reviews_over_time = df.groupby("Year-Month").size().reset_index(name="Total Reviews")
    reviews_over_time["Year-Month"] = pd.to_datetime(reviews_over_time["Year-Month"])
    reviews_over_time = reviews_over_time.sort_values("Year-Month")
    reviews_over_time.set_index("Year-Month", inplace=True)
    st.subheader("📈 Reviews Over Time & Forecast")
    # User input for forecast periods
    forecast_periods = st.slider("Select forecast horizon (months):", 3, 24, 12)
    
    # Apply Exponential Smoothing Model
    model = ExponentialSmoothing(
        reviews_over_time["Total Reviews"], 
        trend="add", seasonal="add", seasonal_periods=12
    )
    fit = model.fit()
    
    # Compute Confidence Intervals
    future_dates = pd.date_range(start=reviews_over_time.index[-1], periods=forecast_periods+1, freq="M")[1:]
    future_predictions = fit.forecast(forecast_periods)
    conf_int = 1.96 * np.std(fit.resid)
    upper_bound = future_predictions + conf_int
    lower_bound = future_predictions - conf_int
    
    forecast_df = pd.DataFrame({
        "Year-Month": future_dates, 
        "Total Reviews": future_predictions,
        "Upper Bound": upper_bound,
        "Lower Bound": lower_bound
    })
    
    # Merge past and future data
    full_data = pd.concat([reviews_over_time.reset_index(), forecast_df])
    
    # Model Performance Metrics
    actual = reviews_over_time["Total Reviews"][-forecast_periods:]
    predicted = fit.fittedvalues[-forecast_periods:]
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    
    st.write(f"**Model Performance:**")
    st.write(f"- Mean Absolute Error (MAE): {mae:.2f}")
    st.write(f"- Root Mean Squared Error (RMSE): {rmse:.2f}")
    
    # Plot Forecast
    fig_forecast = px.line(full_data, x="Year-Month", y="Total Reviews", title="Reviews Over Time & Forecast")
    fig_forecast.add_scatter(x=future_dates, y=future_predictions, mode="lines", name="Forecast", line=dict(dash="dot"))
    fig_forecast.add_scatter(x=future_dates, y=upper_bound, mode="lines", name="Upper Bound", line=dict(dash="dash", color='green'))
    fig_forecast.add_scatter(x=future_dates, y=lower_bound, mode="lines", name="Lower Bound", line=dict(dash="dash", color='red'))
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    # Time Series Decomposition
    st.subheader("📊 Time Series Decomposition")
    decomposition = seasonal_decompose(reviews_over_time["Total Reviews"], model='additive', period=12)
    
    fig_trend = px.line(x=reviews_over_time.index, y=decomposition.trend, title="Trend Component")
    fig_seasonal = px.line(x=reviews_over_time.index, y=decomposition.seasonal, title="Seasonal Component")
    fig_residual = px.line(x=reviews_over_time.index, y=decomposition.resid, title="Residual Component")
    
    st.plotly_chart(fig_trend, use_container_width=True)
    st.plotly_chart(fig_seasonal, use_container_width=True)
    st.plotly_chart(fig_residual, use_container_width=True)
    
    # Rolling Average
    st.subheader("📈 Rolling Average")
    reviews_over_time['Rolling Avg'] = reviews_over_time["Total Reviews"].rolling(window=3).mean()
    fig_rolling = px.line(reviews_over_time, x=reviews_over_time.index, y="Rolling Avg", title="3-Month Rolling Average")
    st.plotly_chart(fig_rolling, use_container_width=True)
