"""
data_loader.py
Pulls stock and market price data and computes returns for CAPM analysis.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import os

def download_prices(ticker: str, start: str, end: str) -> pd.Series:
    """
    Downloads adjusted close prices for a given ticker.
    """
    data = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
    return data["Close"]


def compute_returns(prices: pd.Series, freq: str = "W") -> pd.Series:
    """
    Resamples prices to the given frequency and computes simple returns.
    freq: 'D' for daily, 'W' for weekly, 'M' for monthly
    """
    resampled = prices.resample(freq).last()
    returns = resampled.pct_change().dropna()
    return returns


def build_dataset(stock_ticker: str, market_ticker: str, start: str, end: str, freq: str = "W") -> pd.DataFrame:
    """
    Builds a combined DataFrame of stock and market returns, aligned on date.
    """
    stock_prices = download_prices(stock_ticker, start, end)
    market_prices = download_prices(market_ticker, start, end)

    stock_returns = compute_returns(stock_prices, freq)
    market_returns = compute_returns(market_prices, freq)

    df = pd.concat([stock_returns, market_returns], axis=1)
    df.columns = ["stock_return", "market_return"]
    df = df.dropna()

    return df


if __name__ == "__main__":
    STOCK = "AAPL"       # ticker
    MARKET = "^GSPC"     # S&P 500
    START = "2015-01-01"
    END = "2025-01-01"
    FREQ = "W"

    df = build_dataset(STOCK, MARKET, START, END, FREQ)

    os.makedirs("data", exist_ok=True)
    out_path = f"data/{STOCK}_returns.csv"
    df.to_csv(out_path)
    print(f"Saved {len(df)} rows of return data to {out_path}")
    print(df.head())
