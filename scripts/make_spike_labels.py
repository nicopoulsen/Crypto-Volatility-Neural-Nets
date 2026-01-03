import pandas as pd
import numpy as np

IN_PATH = "data/btc_cadli_hourly_with_indicators.csv"
OUT_PATH = "data/btc_cadli_hourly_with_indicators_labeled.csv"

HORIZON_HOURS = 3
THRESH_QUANTILE = 0.99
TRAIN_END = "2023-12-31 23:00:00+00:00"

df = pd.read_csv(IN_PATH, parse_dates=["datetime"], index_col="datetime").sort_index()

threshold = df.loc[:TRAIN_END, "abs_return_1h"].quantile(THRESH_QUANTILE)

future_max = (
    df["abs_return_1h"]
    .shift(-1)
    .rolling(window=HORIZON_HOURS, min_periods=HORIZON_HOURS)
    .max()
)

df["future_max_abs_return_h"] = future_max
df["spike"] = (df["future_max_abs_return_h"] >= threshold).astype(int)

future_ret = df["log_return_1h"].shift(-1).to_numpy()
future_abs = df["abs_return_1h"].shift(-1).to_numpy()

dir_out = np.full(len(df), np.nan)
for i in range(len(df) - HORIZON_HOURS):
    w_abs = future_abs[i : i + HORIZON_HOURS]
    j = int(np.argmax(w_abs))
    dir_out[i] = np.sign(future_ret[i + j])

df["spike_direction"] = dir_out
df.loc[df["spike"] == 0, "spike_direction"] = 0
df["spike_direction"] = df["spike_direction"].astype("Int64")

df = df.iloc[:-HORIZON_HOURS]
df.to_csv(OUT_PATH)
