# Multi-Factor Asset Pricing & Return Attribution

A reproducible quantitative equity research project testing whether lagged momentum, volatility, volume and intraday-range factors explain or predict cross-sectional U.S. equity returns. The emphasis is on factor construction, chronological validation and honest reporting of weak out-of-sample evidence.

## Result snapshot

| Evidence | Historical reference result |
| --- | ---: |
| Raw OHLCV observations | 619,040 |
| Modeling panel | 141,333 rows |
| Fixed universe | 120 equities |
| Untouched test set | 17,640 rows |
| Test R-squared | -0.016 |
| Mean daily rank IC | -0.011 |

**Decision:** the tested factors did not generalize and should not influence portfolio weights without stronger point-in-time data and broader robustness testing. Read the [client-style research brief](RESEARCH_BRIEF.md).

## Research question

Which observable market factors are associated with future cross-sectional equity returns, how stable are those relationships out of sample, and how should a quantitative researcher distinguish explanatory attribution from genuine predictive power?

## Research design

- **Data:** daily OHLCV downloaded at runtime with `yfinance`
- **Universe:** fixed list of 120 liquid U.S. equities in `data/universe.csv`
- **Factors:** 5/20/60-day momentum, 20-day volatility, relative volume and intraday range
- **Model:** Ridge regression with standardized predictors
- **Target:** next-period close-to-close return
- **Validation:** chronological train/validation/test split
- **Evaluation:** out-of-sample R-squared and mean daily Spearman rank IC

All features are shifted by one trading day. Predictors therefore never use information from the return period they are asked to predict.

## Reproduce

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/run_analysis.py --start 2010-01-01 --end 2026-01-01
```

The run writes downloaded data to `data/raw/ohlcv.parquet`, test predictions to `outputs/test_predictions.csv`, and metrics to `outputs/metrics.json`. The committed `outputs/reference_metrics.json` records the historical reference run separately so updated market data is never confused with the original evidence.

## Start-to-finish workflow

1. Fix the universe before evaluation and validate ticker coverage.
2. Download and clean adjusted OHLCV history.
3. engineer lagged momentum, volatility, volume and range factors.
4. Build the stock-date panel and remove incomplete histories.
5. Split dates chronologically into training, validation and untouched test periods.
6. Standardize features using training-era information and fit Ridge regression.
7. Evaluate only after model specification using R-squared and daily rank IC.
8. Preserve negative findings and document leakage, survivorship and implementation risks.

## Repository map

- `src/run_analysis.py` - end-to-end research pipeline
- `data/universe.csv` - fixed 120-stock universe
- `outputs/reference_metrics.json` - documented historical evidence
- `RESEARCH_BRIEF.md` - executive interpretation and portfolio implication
- `requirements.txt` - reproducible Python dependencies

## Limitations

The fixed present-day universe can create survivorship bias. Yahoo data is not institutional point-in-time data, Ridge captures only linear structure, and statistical signal does not imply tradable alpha after transaction costs, market impact or capacity constraints.
