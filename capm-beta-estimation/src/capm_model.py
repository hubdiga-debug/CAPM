"""
capm_model.py
Static and rolling CAPM regression functions.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm


def run_static_capm(df: pd.DataFrame) -> dict:
    """
    Runs a single OLS regression over the full sample:
    stock_return = alpha + beta * market_return + epsilon

    Returns a dict with beta, alpha, r_squared, and the fitted model object.
    """
    X = sm.add_constant(df["market_return"])
    y = df["stock_return"]

    model = sm.OLS(y, X).fit()

    return {
        "alpha": model.params["const"],
        "beta": model.params["market_return"],
        "r_squared": model.rsquared,
        "p_value_beta": model.pvalues["market_return"],
        "model": model,
    }


def run_rolling_capm(df: pd.DataFrame, window: int = 52) -> pd.DataFrame:
    """
    Runs a rolling OLS regression to estimate time-varying beta.
    window: number of periods in each rolling window (e.g., 52 weeks = 1 year)

    Returns a DataFrame indexed by date with rolling alpha, beta, and r_squared.
    """
    results = []
    dates = []

    for i in range(window, len(df) + 1):
        window_df = df.iloc[i - window:i]
        X = sm.add_constant(window_df["market_return"])
        y = window_df["stock_return"]

        model = sm.OLS(y, X).fit()

        results.append({
            "alpha": model.params["const"],
            "beta": model.params["market_return"],
            "r_squared": model.rsquared,
        })
        dates.append(df.index[i - 1])

    rolling_df = pd.DataFrame(results, index=dates)
    return rolling_df


if __name__ == "__main__":
    # Example usage — assumes data already saved by data_loader.py
    df = pd.read_csv("data/AAPL_returns.csv", index_col=0, parse_dates=True)

    static_result = run_static_capm(df)
    print("Static CAPM Results")
    print(f"  Alpha: {static_result['alpha']:.5f}")
    print(f"  Beta:  {static_result['beta']:.3f}")
    print(f"  R²:    {static_result['r_squared']:.3f}")
    print(f"  Beta p-value: {static_result['p_value_beta']:.4f}")

    rolling_result = run_rolling_capm(df, window=52)
    rolling_result.to_csv("outputs/rolling_beta.csv")
    print(f"\nRolling beta saved to outputs/rolling_beta.csv")
    print(rolling_result.tail())
