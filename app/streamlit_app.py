import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytz
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from src.data_fetcher import fetch_alpha_intraday
from src.indicators import sma, ema, rsi
from src.plotting import plot_candlestick, add_linear_trendline

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Real-Time Stock Market Analysis",
    page_icon="📈",
    layout="wide"
)

# ---------------------------
# SIDEBAR SETTINGS
# ---------------------------
st.sidebar.header("⚙️ Settings")

# WATCHLIST = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "INFY", "RELIANCE.BSE", "TCS.BSE"]

# Load watchlist
watchlist = pd.read_csv("data\watchlist.csv")

# Dropdown of all stocks
symbol = st.sidebar.selectbox(
    "Select Symbol",
    options=watchlist["symbol"].tolist(),
    format_func=lambda x: f"{x} - {watchlist.loc[watchlist['symbol']==x, 'name'].values[0]}"
)

interval = st.sidebar.selectbox(
    "Interval",
    ["1min", "5min", "15min", "60min"],
    index=0
)

sma_periods = st.sidebar.multiselect("SMA Periods", [10, 20, 50, 100], default=[20, 50])
ema_periods = st.sidebar.multiselect("EMA Periods", [10, 20, 50, 100], default=[20])
show_rsi = st.sidebar.checkbox("Show RSI (14)", value=True)
show_trendline = st.sidebar.checkbox("Show Trendline", value=False)

timezone = st.sidebar.selectbox(
    "Timezone",
    pytz.all_timezones,
    index=pytz.all_timezones.index("Asia/Kolkata")  # default IST
)

# ---------------------------
# AUTO REFRESH
# ---------------------------
interval_map = {
    "1min": 60 * 1000,
    "5min": 5 * 60 * 1000,
    "15min": 15 * 60 * 1000,
    "60min": 60 * 60 * 1000
}
refresh_ms = interval_map[interval]

st_autorefresh(interval=refresh_ms, key="refresh")

# ---------------------------
# DATA FETCHING
# ---------------------------
@st.cache_data(ttl=60)  # cache for 60s (safe with free API limits)
def get_data(symbol, interval, tz):
    return fetch_alpha_intraday(symbol, interval=interval, tz=tz)

try:
    df = get_data(symbol, interval, timezone)
except Exception as e:
    st.error(f"❌ Error fetching data: {e}")
    st.stop()

# ---------------------------
# INDICATORS
# ---------------------------
for p in sma_periods:
    df[f"SMA_{p}"] = sma(df["close"], p)
for p in ema_periods:
    df[f"EMA_{p}"] = ema(df["close"], p)
if show_rsi:
    df["RSI_14"] = rsi(df["close"], 14)

# ---------------------------
# VISUALIZATION
# ---------------------------
st.title("📊 Real-Time Trading / Stock Market Analysis")

fig = plot_candlestick(
    df,
    sma_periods=sma_periods,
    ema_periods=ema_periods,
    title=f"{symbol} - {interval}"
)

if show_trendline:
    add_linear_trendline(fig, df, window=100, name="Trend (last 100)")

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# KPIs
# ---------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Last Price", f"{df['close'].iloc[-1]:.2f}",
            delta=f"{(df['close'].pct_change().iloc[-1] * 100):.2f}%")
if "RSI_14" in df and show_rsi:
    col2.metric("RSI (14)", f"{df['RSI_14'].iloc[-1]:.2f}")
col3.metric("Volume", f"{df['volume'].iloc[-1]:,.0f}")

# ---------------------------
# DATA TABLE
# ---------------------------
st.subheader("📑 Recent Data")
st.dataframe(df.tail(50))
