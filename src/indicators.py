import pandas as pd
import numpy as np

def sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(window=period).mean()

def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()

def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def volatility(series: pd.Series, period: int = 20, annualize_factor: float = None) -> pd.Series:
    logret = np.log(series / series.shift(1))
    vol = logret.rolling(window=period).std()
    if annualize_factor:
        vol = vol * np.sqrt(annualize_factor)
    return vol
