import pandas as pd
import numpy as np

data_path = "data/btc_cadli_hourly.csv"
out_path = "data/btc_cadli_hourly_with_indicators.csv"

df = pd.read_csv(
    data_path,
    parse_dates=["datetime"],
    index_col="datetime"
)

num_cols = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "QUOTE_VOLUME"]
for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df["log_return_1h"] = np.log(df["CLOSE"]).diff()
df["abs_return_1h"] = df["log_return_1h"].abs()

df["vol_6h"] = df["log_return_1h"].rolling(6).std()
df["vol_12h"] = df["log_return_1h"].rolling(12).std()
df["vol_24h"] = df["log_return_1h"].rolling(24).std()

df["volume_change"] = df["VOLUME"].pct_change()
df["volume_ma_24h"] = df["VOLUME"].rolling(24).mean()
df["volume_ratio"] = df["VOLUME"] / df["volume_ma_24h"]

# RSI (14)
delta = df["CLOSE"].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss
df["rsi_14"] = 100 - (100 / (1 + rs))

# MACD  for (12, 26, 9)
ema_12 = df["CLOSE"].ewm(span=12, adjust=False).mean()
ema_26 = df["CLOSE"].ewm(span=26, adjust=False).mean()

df["macd"] = ema_12 - ema_26
df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()

df = df.dropna()

df.to_csv(out_path)