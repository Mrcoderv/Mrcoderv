"""
Nepal Stock Exchange (NEPSE) Real-time Chart Analysis
Author: Raghav Panthi (Mrcoderv)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta
import time
import json

# Page configuration
st.set_page_config(
    page_title="NEPSE Real-time Chart Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🏛️ Nepal Stock Exchange (NEPSE) Real-time Analysis")
    st.markdown("---")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Live Charts", "Technical Analysis", "Stock Screener", "Portfolio Tracker"]
    )
    
    if page == "Live Charts":
        show_live_charts()
    elif page == "Technical Analysis":
        show_technical_analysis()
    elif page == "Stock Screener":
        show_stock_screener()
    elif page == "Portfolio Tracker":
        show_portfolio_tracker()

def show_live_charts():
    st.header("📊 Live Stock Charts")
    
    # For now, we'll create sample data since we need to research actual NEPSE APIs
    st.warning("⚠️ Currently displaying sample data. Real NEPSE API integration in progress.")
    
    # Sample stock symbols (common NEPSE stocks)
    symbols = ["NABIL", "SCB", "EBL", "BOKL", "NICA", "PRVU", "GBIME", "CBL", "SANIMA", "MBL"]
    
    selected_symbol = st.selectbox("Select Stock Symbol", symbols)
    
    # Generate sample data for demonstration
    sample_data = generate_sample_stock_data(selected_symbol)
    
    # Display current price
    current_price = sample_data['Close'].iloc[-1]
    prev_price = sample_data['Close'].iloc[-2]
    change = current_price - prev_price
    change_percent = (change / prev_price) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Price", f"Rs. {current_price:.2f}")
    with col2:
        st.metric("Change", f"Rs. {change:.2f}", f"{change_percent:.2f}%")
    with col3:
        st.metric("High", f"Rs. {sample_data['High'].iloc[-1]:.2f}")
    with col4:
        st.metric("Low", f"Rs. {sample_data['Low'].iloc[-1]:.2f}")
    
    # Candlestick chart
    fig = create_candlestick_chart(sample_data, selected_symbol)
    st.plotly_chart(fig, use_container_width=True)
    
    # Volume chart
    volume_fig = create_volume_chart(sample_data)
    st.plotly_chart(volume_fig, use_container_width=True)

def show_technical_analysis():
    st.header("🔍 Technical Analysis")
    st.info("Technical indicators and analysis tools will be implemented here.")
    
    # Placeholder for technical analysis features
    st.subheader("Available Indicators")
    indicators = ["Moving Averages", "RSI", "MACD", "Bollinger Bands", "Stochastic"]
    for indicator in indicators:
        st.checkbox(indicator)

def show_stock_screener():
    st.header("🔎 Stock Screener")
    st.info("Stock screening and filtering tools will be implemented here.")

def show_portfolio_tracker():
    st.header("💼 Portfolio Tracker")
    st.info("Portfolio tracking and performance analysis will be implemented here.")

def generate_sample_stock_data(symbol, days=30):
    """Generate sample stock data for demonstration"""
    dates = pd.date_range(start=datetime.now() - timedelta(days=days), end=datetime.now(), freq='D')
    
    # Start with a base price and add random walk
    base_price = np.random.uniform(200, 1000)
    prices = [base_price]
    
    for i in range(1, len(dates)):
        change = np.random.normal(0, base_price * 0.02)  # 2% volatility
        new_price = max(prices[-1] + change, 1)  # Ensure price doesn't go negative
        prices.append(new_price)
    
    # Generate OHLC data
    data = []
    for i, (date, close) in enumerate(zip(dates, prices)):
        high = close * np.random.uniform(1.001, 1.05)
        low = close * np.random.uniform(0.95, 0.999)
        open_price = prices[i-1] if i > 0 else close
        volume = np.random.randint(1000, 50000)
        
        data.append({
            'Date': date,
            'Open': open_price,
            'High': high,
            'Low': low,
            'Close': close,
            'Volume': volume
        })
    
    return pd.DataFrame(data)

def create_candlestick_chart(data, symbol):
    """Create candlestick chart with plotly"""
    fig = go.Figure(data=go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name=symbol
    ))
    
    fig.update_layout(
        title=f"{symbol} - Candlestick Chart",
        yaxis_title="Price (Rs.)",
        xaxis_title="Date",
        height=500,
        template="plotly_dark"
    )
    
    return fig

def create_volume_chart(data):
    """Create volume chart"""
    fig = go.Figure(data=go.Bar(
        x=data['Date'],
        y=data['Volume'],
        name="Volume",
        marker_color='lightblue'
    ))
    
    fig.update_layout(
        title="Trading Volume",
        yaxis_title="Volume",
        xaxis_title="Date",
        height=300,
        template="plotly_dark"
    )
    
    return fig

if __name__ == "__main__":
    main()