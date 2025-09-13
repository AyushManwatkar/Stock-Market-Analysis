import plotly.graph_objects as go
import numpy as np

def plot_candlestick(df, sma_periods=None, ema_periods=None, title=""):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index, open=df["open"], high=df["high"], low=df["low"], close=df["close"], name="price"
    ))
    if sma_periods:
        for p in sma_periods:
            if f"SMA_{p}" in df:
                fig.add_trace(go.Scatter(x=df.index, y=df[f"SMA_{p}"], name=f"SMA {p}", mode="lines"))
    if ema_periods:
        for p in ema_periods:
            if f"EMA_{p}" in df:
                fig.add_trace(go.Scatter(x=df.index, y=df[f"EMA_{p}"], name=f"EMA {p}", mode="lines"))
    fig.update_layout(title=title, xaxis_rangeslider_visible=False)
    return fig

def add_linear_trendline(fig, df, window=None, name="trend"):
    sub = df if window is None else df.tail(window)
    if len(sub) < 2:
        return
    x = np.arange(len(sub))
    y = sub["close"].values
    p = np.polyfit(x, y, 1)
    trend = p[0] * x + p[1]
    fig.add_trace(go.Scatter(x=sub.index, y=trend, name=name, line=dict(dash="dash")))
