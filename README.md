# Multi-Factor Asset Pricing & Return Attribution

A reproducible quantitative equity research project testing whether lagged momentum, volatility, volume and intraday-range factors explain or predict cross-sectional U.S. equity returns. The emphasis is on factor construction, risk/return attribution, chronological validation and honest reporting of weak out-of-sample evidence.

## Research question

Which observable market factors are associated with future cross-sectional equity returns, how stable are those relationships out of sample, and how should a quantitative researcher distinguish explanatory attribution from genuine predictive power?

## Skills demonstrated

- Multi-factor return modeling and asset-pricing intuition
- Cross-sectional return prediction
- Factor exposure and coefficient interpretation
- Regularized regression
- Chronological train/validation/test design
- Rank information coefficient and quintile spread analysis
- Python, Pandas, NumPy and scikit-learn
- Leakage control, research documentation and model-risk awareness

## Research design

- **Data:** daily OHLCV downloaded at runtime with `yfinance`
- **Universe:** fixed list of 120 liquid U.S. equities in `data/universe.csv`
- **Factors:** 5/20/60-day momentum, 20-day volatility, relative volume and intraday range
- **Model:** Ridge regression with standardized predictors
- **Target:** next-period close-to-close return
- **Validation:** chronological train/validation/test split
- **Evaluation:** out-of-sample R-squared, MAE and mean daily Spearman rank IC

All features are shifted by one trading day. Predictors therefore never use information from the return period they are asked to explain or predict.

## Start-to-finish workflow

1. Define a liquid equity universe before model evaluation.
2. Download adjusted OHLCV history and validate ticker coverage.
3. Create lagged momentum, realized-volatility, relative-volume and range factors.
4. Shift every feature so no target-period information leaks into predictors.
5. Build a stock-date modeling panel and remove rows lacking required history.
6. Split observations chronologically into training, validation and untouched test periods.
7. Standardize features and fit Ridge regression using only training-era information.
8. Select regularization strength with validation-period results rather than test performance.
9. Evaluate the final model on the untouched test period.
10. Report regression fit, prediction error, daily rank IC and factor coefficients.
11. Compare top-versus-bottom factor/model ranks to assess cross-sectional separation.
12. Preserve negative findings rather than optimizing the research narrative around a favorable result.

## Historical reference result

An earlier run used **619,040 raw OHLCV records**, a **141,333-row modeling panel** and a **17,640-row untouched test set**. It reported test R-squared of **-0.016** and mean daily rank IC of **-0.011**. Those weak results are deliberately retained because they demonstrate that simple technical factors did not generalize out of sample in that experiment.

These are historical reference results, not hard-coded outputs. Re-run the pipeline and report the newly produced metrics with the retrieval date.

## Run

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/run_analysis.py --start 2010-01-01 --end 2026-01-01
```

Outputs are written to `outputs/`. Market data is not committed because redistributed adjusted histories may change.

## Why this matters for portfolio research

Factor coefficients and cross-sectional ranks provide a transparent way to ask whether observed characteristics contain information about relative returns. The project also demonstrates a critical institutional-research lesson: statistical relationships must survive chronological out-of-sample testing before they should influence portfolio construction.

## Limitations

The fixed present-day universe can create survivorship bias. Yahoo data is not institutional point-in-time data, Ridge captures only linear structure, and statistical signal does not imply tradeable alpha after transaction costs, market impact or capacity constraints.

## Resume-ready description

**Multi-Factor Asset Pricing & Return Attribution | Python, Pandas, scikit-learn**

Engineered lagged momentum, volatility, volume and range factors across a 120-stock universe and fit a regularized cross-sectional return model using chronological train/validation/test periods. Evaluated out-of-sample R-squared, prediction error and rank IC, retained weak test results rather than overfitting, and documented leakage, survivorship and implementation limitations.
