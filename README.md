# Large-Scale Equity Factor Analysis and Return Prediction

This project tests whether simple lagged price, volatility, volume, and intraday-range factors predict next-period cross-sectional U.S. equity returns.

## Research design

- Data: daily OHLCV downloaded at runtime with `yfinance`
- Universe: fixed list of 120 liquid U.S. equities in `data/universe.csv`
- Features: 5/20/60-day momentum, 20-day volatility, relative volume, and intraday range
- Model: Ridge regression with standardized predictors
- Validation: chronological train/validation/test split
- Evaluation: out-of-sample R² and mean daily Spearman rank IC

All features are shifted by one trading day. The target is the next close-to-close return, so predictors never use information from the target period.

## Resume reference result

The earlier analysis summarized on the résumé used 619,040 raw OHLCV records, a 141,333-row modeling panel, and a 17,640-row untouched test set. It reported test R² of -0.016 and mean daily rank IC of -0.011. These are historical reference results, not hard-coded outputs. Re-run the pipeline and report the newly produced metrics with the data retrieval date.

## Run

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/run_analysis.py --start 2010-01-01 --end 2026-01-01
```

The script downloads data into `data/raw/` and writes metrics and predictions to `outputs/`. Market data is not committed because redistribution terms and adjusted histories may change.

## Limitations

The fixed present-day universe can create survivorship bias. Yahoo data may be revised and is not institutional point-in-time data. Ridge captures only linear structure, and statistical results do not establish tradeable performance after costs.

## Next tests

Walk-forward validation, sector-neutral ranks, nonlinear interactions, delisted securities, regime stability, and explicit turnover/slippage analysis.