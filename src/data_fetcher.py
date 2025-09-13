import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
ALPHA_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
ALPHA_URL = "https://www.alphavantage.co/query"

def fetch_alpha_intraday(symbol:str,interval:str="1min",outputsize:str="compact",tz:str="Asia/Kolkata")->pd.DataFrame:
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": ALPHA_KEY
    }
    r = requests.get(ALPHA_URL, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()

    if "Note" in data:
        raise RuntimeError("AlphaVantage rate limit: " + data["Note"])
    if "Error Message" in data:
        raise RuntimeError("AlphaVantage error: " + data["Error Message"])

    ts_key = next((k for k in data.keys() if "Time Series" in k), None)
    if ts_key is None:
        raise RuntimeError("Unexpected response keys: " + ", ".join(data.keys()))

    ts = data[ts_key]
    df = pd.DataFrame.from_dict(ts, orient="index")
    df.columns = [c.split(". ")[1] for c in df.columns]
    df = df.astype(float)

    # Convert to datetime + timezone
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    # AlphaVantage = US Eastern Time (ET)
    df.index = df.index.tz_localize("US/Eastern").tz_convert(tz)

    df = df.rename(columns={"open": "open", "high": "high", "low": "low", "close": "close", "volume": "volume"})
    return df[["open", "high", "low", "close", "volume"]]