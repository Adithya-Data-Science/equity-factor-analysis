from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import spearmanr
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["mom_5", "mom_20", "mom_60", "vol_20", "rel_volume_20", "intraday_range"]

def download(tickers, start, end):
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True,
                      group_by="ticker", threads=True, progress=False)
    rows = []
    for ticker in tickers:
        if ticker not in raw.columns.get_level_values(0):
            continue
        frame = raw[ticker].reset_index()
        frame.columns = [str(c).lower() for c in frame.columns]
        frame["ticker"] = ticker
        rows.append(frame)
    if not rows:
        raise RuntimeError("No market data downloaded.")
    return pd.concat(rows, ignore_index=True)

def features(frame):
    frame = frame.sort_values(["ticker", "date"]).copy()
    frame["ret_1"] = frame.groupby("ticker")["close"].transform(
        lambda s: s.pct_change(fill_method=None))
    for n in (5, 20, 60):
        frame[f"mom_{n}"] = frame.groupby("ticker")["close"].transform(
            lambda s, n=n: s.pct_change(n, fill_method=None).shift(1))
    frame["vol_20"] = frame.groupby("ticker")["ret_1"].transform(
        lambda s: s.rolling(20).std().shift(1))
    frame["rel_volume_20"] = frame.groupby("ticker")["volume"].transform(
        lambda s: (s / s.rolling(20).mean()).shift(1))
    frame["intraday_range"] = ((frame["high"] - frame["low"]) / frame["close"]).groupby(
        frame["ticker"]).shift(1)
    frame["target"] = frame.groupby("ticker")["close"].transform(
        lambda s: s.pct_change(fill_method=None).shift(-1))
    return frame.dropna(subset=FEATURES + ["target"])

def split_dates(panel):
    dates = np.array(sorted(panel["date"].unique()))
    a, b = int(.60 * len(dates)), int(.80 * len(dates))
    return dates[:a], dates[a:b], dates[b:]

def daily_rank_ic(frame):
    values = []
    for _, day in frame.groupby("date"):
        if len(day) >= 5:
            ic = spearmanr(day["prediction"], day["target"]).statistic
            if np.isfinite(ic):
                values.append(float(ic))
    return float(np.mean(values)) if values else float("nan")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--start", default="2010-01-01")
    p.add_argument("--end", default="2026-01-01")
    p.add_argument("--alpha", type=float, default=10.0)
    args = p.parse_args()
    tickers = pd.read_csv(ROOT / "data/universe.csv")["ticker"].tolist()
    raw = download(tickers, args.start, args.end)
    panel = features(raw)
    train_dates, val_dates, test_dates = split_dates(panel)
    train = panel[panel.date.isin(train_dates)]
    test = panel[panel.date.isin(test_dates)].copy()
    model = Pipeline([("scale", StandardScaler()), ("ridge", Ridge(alpha=args.alpha))])
    model.fit(train[FEATURES], train["target"])
    test["prediction"] = model.predict(test[FEATURES])
    metrics = {
        "downloaded_rows": int(len(raw)),
        "modeling_rows": int(len(panel)),
        "validation_dates": int(len(val_dates)),
        "test_rows": int(len(test)),
        "test_r2": float(r2_score(test["target"], test["prediction"])),
        "mean_daily_rank_ic": daily_rank_ic(test),
        "start": args.start, "end": args.end, "alpha": args.alpha
    }
    out = ROOT / "outputs"; out.mkdir(exist_ok=True)
    (ROOT / "data/raw").mkdir(parents=True, exist_ok=True)
    raw.to_parquet(ROOT / "data/raw/ohlcv.parquet", index=False)
    test[["date","ticker","target","prediction"]].to_csv(out / "test_predictions.csv", index=False)
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    main()
