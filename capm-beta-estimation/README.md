# CAPM Beta Estimation & Rolling Risk Analysis

## Problem Statement
Systematic (market) risk is one of the first things a risk analyst measures for any equity position.
This project estimates a stock's **beta** relative to the market using CAPM, and — more importantly —
tracks how that beta *changes over time*, since real portfolio risk is never static.

**Risk question being answered:** How sensitive is [AAPL] to broad market moves, and has that
sensitivity been stable or has it shifted meaningfully in the last N years?

## Data
- **Stock returns:** [AAPL] daily/weekly adjusted close prices via `yfinance`
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
- The full-period beta is **1.105**, which is statistically significant at the **99%** level (p < 0.01), with the market explaining **47.4%** of the stock's variance (R² = **0.474**).
- Rolling beta ranged from **[0.65]** to **[1.4]** between [Jan 2018] and [Jan 2022]
- Notable regime shift observed



## So What? (Risk Relevance)
Analysis of Major Beta Swings (2016–2025)

The variations you observed are typically driven by a mix of macroeconomic shifts and Apple-specific corporate events:

Oct 2016 (1.45 Peak): This high beta coincided with the launch of the iPhone 7 and recovery from the 2015-16 global growth scare. Higher beta here reflected aggressive growth sentiment as Apple integrated more deeply into the broader tech rally.

Jan 2018 (0.65 Trough): Apple became significantly "less risky" than the market. This low point followed the stable iPhone X launch and massive tax reform benefits, positioning it as a safe-haven "cash cow" during early 2018 market jitters.

March – June 2020 (1.05 to 0.95 Drop): During the initial COVID-19 crash, Apple’s beta briefly dropped as investors treated its massive cash reserves as a defensive buffer against more vulnerable sectors.

June 2020 – Jan 2022 (1.42 Highs): These peaks align with the "Work from Home" tech boom. As Apple's market cap surged toward $3 trillion, its correlation with the S&P 500 intensified, causing it to move more aggressively in tandem with (or ahead of) the broader index.


Sept/Oct 2023 (1.4 High): This spike likely reflected market anxiety over interest rate hikes and specific supply chain concerns in China, which made Apple's stock more sensitive to global macro news than usual.

Jan 2025 (0.85 Low): A lower beta in early 2025 suggests a period of relative stability or "sideways" trading where Apple decoupled from broader market volatility, perhaps as investors awaited the impact of AI-integrated service

## How to Run
```bash
pip install -r requirements.txt
python src/data_loader.py
jupyter notebook notebooks/capm_analysis.ipynb
```

## Next Steps / Extensions
- Extend to multi-factor (Fama-French) —> see companion project
- Add a second stock for comparison (e.g., high-beta tech vs. low-beta utility)
- Test beta stability formally (Chow test at suspected regime-shift points)
