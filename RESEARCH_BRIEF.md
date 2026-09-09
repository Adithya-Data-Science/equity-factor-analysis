# Research Brief: Do Simple Technical Factors Generalize?

## Executive conclusion

In the historical reference run, a regularized cross-sectional model using lagged momentum, volatility, relative volume, and intraday range did **not** generalize to the untouched test period. Across 120 liquid U.S. equities, the experiment produced 619,040 raw observations, a 141,333-row modeling panel, and 17,640 test observations. Test R-squared was **-0.016** and mean daily rank IC was **-0.011**.

The practical conclusion is not that factor research is useless. It is that these simple technical factors, in this specification and universe, should not be used for portfolio allocation without stronger point-in-time data, broader robustness analysis, and evidence that survives costs.

## Research design

- Universe fixed before evaluation: 120 liquid U.S. equities
- Features: lagged 5-, 20-, and 60-day momentum; 20-day volatility; relative volume; intraday range
- Model: standardized Ridge regression
- Validation: chronological train, validation, and untouched test periods
- Controls: one-day feature lag and no test-period model selection
- Evaluation: out-of-sample R-squared and daily Spearman rank information coefficient

## Client and portfolio implication

A client portfolio process should treat intuitive technical signals as hypotheses rather than expected alpha. This result supports three controls: require point-in-time data, compare results across market regimes and universes, and establish an explicit promotion threshold before a signal can influence portfolio weights.

## Limitations

The present-day universe creates survivorship risk; Yahoo data is not institutional point-in-time data; the model is linear; transaction costs, capacity, and market impact are excluded. Results are research evidence, not investment advice.
