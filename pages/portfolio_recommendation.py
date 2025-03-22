import os
import requests
import streamlit as st
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import sys
sys.path.append(r"C:\Users\DELL\OneDrive\Documents\robo")
from portfolio_optimizer import get_stock_data, mean_variance_optimization  # Import optimization functions

# Load API Key from .env
load_dotenv()
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Define API URLs
POLYGON_BASE_URL = "https://api.polygon.io/v3/reference/tickers"
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

# Streamlit App Title
st.title("📊 AI-Driven Portfolio Recommendation")
st.write("Optimize your stock portfolio using AI-driven insights!")

# User Risk Tolerance Selection
risk_tolerance = st.selectbox("Select your risk tolerance:", ["Low", "Medium", "High"])

# Function to fetch stock symbols from Polygon API
def get_stock_tickers():
    params = {
        "market": "stocks",
        "active": "true",
        "order": "asc",
        "limit": 10,
        "sort": "ticker",
        "apiKey": POLYGON_API_KEY
    }
    response = requests.get(POLYGON_BASE_URL, params=params)
    if response.status_code == 200:
        return [ticker["ticker"] for ticker in response.json().get("results", [])]
    else:
        return []

# Function to fetch stock symbols from Alpha Vantage
def get_alpha_vantage_stock_symbols():
    params = {"function": "LISTING_STATUS", "apikey": ALPHA_VANTAGE_API_KEY}
    response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
    if response.status_code == 200:
        stock_list = response.text.split("\n")
        return [row.split(",")[0] for row in stock_list if row][:10]
    else:
        return []

# Fetch stock symbols from both sources
polygon_symbols = get_stock_tickers()
av_symbols = get_alpha_vantage_stock_symbols()

# Merge and display stock symbols
suggested_assets = list(set(polygon_symbols + av_symbols))
if not suggested_assets:
    st.error("❌ No stock symbols available.")
    st.stop()

st.write(f"### Suggested Stocks: {', '.join(suggested_assets)}")

# Fetch historical stock data
try:
    stock_data = get_stock_data(suggested_assets)
    st.success("✅ Stock data loaded successfully!")
except Exception as e:
    st.error(f"❌ Error loading stock data: {e}")
    st.stop()

# Adjust risk preference in optimization
risk_free_rate = 0.02 if risk_tolerance == "Low" else 0.04 if risk_tolerance == "Medium" else 0.06
optimized_weights = mean_variance_optimization(pd.DataFrame({s: stock_data[s]["Adj Close"] for s in stock_data}), risk_free_rate)

# Display portfolio allocation
st.write("### Optimized Portfolio Allocation")
for asset, weight in optimized_weights.items():
    st.write(f"✅ {asset}: {weight:.2%}")