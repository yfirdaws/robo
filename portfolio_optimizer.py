import os
import numpy as np
import pandas as pd
import requests
import streamlit as st
import yfinance as yf
from scipy.optimize import minimize
from dotenv import load_dotenv

# Load API Key securely
load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"

def get_stock_symbols():
    """Fetch stock symbols from Alpha Vantage"""
    try:
        response = requests.get(ALPHA_VANTAGE_URL, params={
            "function": "LISTING_STATUS",
            "apikey": API_KEY
        })
        response.raise_for_status()
        df = pd.read_csv(pd.compat.StringIO(response.text))
        return df['symbol'].tolist()[:10]  # Return only first 10 for testing
    except requests.RequestException as e:
        st.error(f"API Request failed: {e}")
    except Exception as e:
        st.error(f"Unexpected error fetching stock symbols: {e}")
    return []

def get_stock_data(symbol):
    """Fetch historical stock data from Yahoo Finance"""
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="5y")
        if df.empty:
            raise ValueError(f"No data available for {symbol}")
        return df['Close']
    except ValueError as e:
        st.warning(e)
    except Exception as e:
        st.error(f"Error fetching stock data for {symbol}: {e}")
    return None

def mean_variance_optimization(stock_prices):
    """Optimize portfolio allocation using Mean-Variance Optimization."""
    if stock_prices.empty:
        st.error("No valid stock data for optimization.")
        return {}
    
    returns = stock_prices.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    num_assets = len(stock_prices.columns)
    initial_weights = np.ones(num_assets) / num_assets
    
    def portfolio_volatility(weights):
        return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
    bounds = [(0, 1) for _ in range(num_assets)]
    optimized = minimize(portfolio_volatility, initial_weights, bounds=bounds, constraints=constraints)
    
    if not optimized.success:
        st.error("Optimization failed. Using equal allocation.")
        return dict(zip(stock_prices.columns, initial_weights))
    
    return dict(zip(stock_prices.columns, optimized.x))

def get_realtime_price(symbol):
    """Fetch real-time stock price using Yahoo Finance."""
    try:
        stock = yf.Ticker(symbol)
        price = stock.history(period='1d')['Close']
        if price.empty:
            raise ValueError(f"No real-time data available for {symbol}")
        return price.iloc[-1]
    except ValueError as e:
        st.warning(e)
    except Exception as e:
        st.error(f"Error fetching real-time price for {symbol}: {e}")
    return None

def main():
    st.title("Stock Portfolio Optimizer")
    selected_symbols = st.multiselect("Select stocks", get_stock_symbols())
    
    if st.button("Optimize Portfolio") and selected_symbols:
        data = {symbol: get_stock_data(symbol) for symbol in selected_symbols}
        df = pd.DataFrame({k: v for k, v in data.items() if v is not None}).dropna()
        
        if not df.empty:
            allocations = mean_variance_optimization(df)
            st.write("### Optimized Portfolio Allocation")
            st.write(allocations)
        else:
            st.error("Not enough data for optimization.")
    
if __name__ == "__main__":
    main()
