import requests
import pandas as pd
import time
from datetime import datetime, timezone

BASE_URL = "https://data-api.coindesk.com/index/cc/v1/historical/hours"

MARKET = "cadli"
INSTRUMENT = "BTC-USD"

API_KEY = "no_key_needed_for_this_endpoint"

LIMIT = 2000          # this is the max allowed by the API (around 83 days worth of data)
SLEEP_SECONDS = 0.2 


def fetch_all_hourly_data(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch hourly OHLCV data from CoinDesk between start_date and end_date.

    start_date, end_date: 'YYYY-MM-DD'
    """
    start_ts = int(datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc).timestamp())
    end_ts = int(datetime.fromisoformat(end_date).replace(tzinfo=timezone.utc).timestamp())

    all_rows = []
    to_ts = end_ts

    while True:
        params = {
            "market": MARKET,
            "instrument": INSTRUMENT,
            "limit": LIMIT,
            "aggregate": 1,
            "fill": "true",
            "response_format": "JSON",
            "to_ts": to_ts,
            "api_key": API_KEY,   # API key as parameter
        }

        r = requests.get(BASE_URL, params=params, timeout=30)
        r.raise_for_status()
        data = r.json().get("Data", [])

        if not data:
            break

        all_rows.extend(data)

        earliest_ts = min(row["TIMESTAMP"] for row in data)

        if earliest_ts <= start_ts:
            break

        # avoiding overlap here
        to_ts = earliest_ts - 3600

        time.sleep(SLEEP_SECONDS)

    df = pd.DataFrame(all_rows)

    df = df.drop_duplicates(subset="TIMESTAMP")

    df = df[(df["TIMESTAMP"] >= start_ts) & (df["TIMESTAMP"] <= end_ts)]

    df["datetime"] = pd.to_datetime(df["TIMESTAMP"], unit="s", utc=True)
    df = df.sort_values("datetime").set_index("datetime")

    keep_cols = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "QUOTE_VOLUME"]
    df = df[keep_cols]

    return df


if __name__ == "__main__":
    df = fetch_all_hourly_data(
        start_date="2021-01-01",
        end_date="2024-12-31"
    )

    print(df.head())
    print(df.tail())
    print(f"Rows fetched: {len(df)}")

    # local save (have commented out parquet incase we decide to use it later (good analysis too)
    df.to_csv("btc_cadli_hourly.csv")
    # df.to_parquet("btc_cadli_hourly.parquet")
