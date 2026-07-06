# CAPM Beta Estimation & Rolling Risk Analysis

## Problem Statement
Systematic (market) risk is one of the first things a risk analyst measures for any equity position.
This project estimates a stock's **beta** relative to the market using CAPM, and — more importantly —
tracks how that beta *changes over time*, since real portfolio risk is never static.

**Risk question being answered:** How sensitive is [TICKER] to broad market moves, and has that
sensitivity been stable or has it shifted meaningfully in the last N years?

## Data
- **Stock returns:** [TICKER] daily/weekly adjusted close prices via `yfinance`
- **Market benchmark:** S&P 500 (^GSPC) via `yfinance`
- **Period:** [e.g., 2015–2025]
- **Frequency:** Weekly returns (reduces noise vs. daily, still enough data points)

## Methodology
1. Pull price data, compute log or simple returns for both stock and market
2. Static CAPM regression over full period:

   R_stock = α + β(R_market) + ε

3. Rolling regression (e.g., 52-week rolling window) to estimate **time-varying beta**
4. Diagnostics: R², t-stats on β, residual plots (checking for heteroskedasticity/autocorrelation)

## Key Files
- `src/data_loader.py` — pulls and cleans price data
- `src/capm_model.py` — static and rolling regression functions
- `notebooks/capm_analysis.ipynb` — full walkthrough with plots and commentary
- `outputs/` — saved charts (rolling beta plot, scatter plot with regression line)

## Findings
> Fill in after running the analysis. Example structure:
- Full-period beta: **[value]** (statistically significant at [X]% level, R² = [value])
- Rolling beta ranged from **[low]** to **[high]** between [date] and [date]
- Notable regime shift observed around [event, e.g., March 2020 / rate hike cycle 2022] —
  beta rose/fell from X to Y, suggesting [interpretation]

## So What? (Risk Relevance)
Static beta is a snapshot — it hides risk regime changes. A risk analyst monitoring this position
would flag [describe a specific risk implication, e.g., "beta increased from 0.9 to 1.4 during
the 2022 drawdown, meaning the position became more market-sensitive exactly when volatility
was rising — a signal that would warrant a review of position sizing or hedging."]

This mirrors how systematic risk exposure is tracked in practice (e.g., MSCI Barra-style factor
monitoring) — a single static number is insufficient; risk teams need to see exposure drift.

## How to Run
```bash
pip install -r requirements.txt
python src/data_loader.py
jupyter notebook notebooks/capm_analysis.ipynb
```

## Next Steps / Extensions
- Extend to multi-factor (Fama-French) — see companion project
- Add a second stock for comparison (e.g., high-beta tech vs. low-beta utility)
- Test beta stability formally (Chow test at suspected regime-shift points)
