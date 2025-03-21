import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize

# Fetch stock data
def get_stock_data(tickers, start="2010-01-01", end="2024-01-01"):
    data = yf.download(tickers, start=start, end=end)['Close']
    return data

# Calculate portfolio metrics
def mean_variance_optimization(stock_data, risk_free_rate=0.02):
    returns = stock_data.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    num_assets = len(mean_returns)

    def portfolio_volatility(weights):
        return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

    def neg_sharpe_ratio(weights):
        portfolio_return = np.dot(weights, mean_returns)
        portfolio_vol = portfolio_volatility(weights)
        return -(portfolio_return - risk_free_rate) / portfolio_vol  # Negative Sharpe Ratio

    # Constraints: Weights must sum to 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))  # Weights between 0 and 1
    initial_guess = num_assets * [1. / num_assets]  # Equal allocation

    # Optimize portfolio
    result = minimize(neg_sharpe_ratio, initial_guess, bounds=bounds, constraints=constraints)
    
    return dict(zip(stock_data.columns, result.x))  # Return optimized weights
