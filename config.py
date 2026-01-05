DATA_DIR = "data"

RAW_DATA = f"{DATA_DIR}/btc_cadli_hourly.csv"
FEATURE_DATA = f"{DATA_DIR}/btc_cadli_hourly_with_indicators.csv"
LABELED_DATA = f"{DATA_DIR}/btc_cadli_hourly_with_indicators_labeled.csv"

LOOKBACK_HOURS = 24
PREDICTION_HORIZON_HOURS = 3
SPIKE_QUANTILE = 0.99

TRAIN_END_DATE = "2023-12-31 23:00:00+00:00"
