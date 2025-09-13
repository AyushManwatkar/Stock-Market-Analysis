# 📊 Real-Time Stock Market Analysis

A real-time stock market analysis dashboard built with **Python**, **Streamlit**, and **Alpha Vantage API**.  
This project allows you to fetch intraday stock data, visualize candlestick charts, compute indicators, and build a simple trading dashboard.

---

## 🚀 Features
- Fetch real-time intraday stock prices from **Alpha Vantage API**.
- Supports multiple intervals: `1min`, `5min`, `15min`, `60min`.
- Candlestick charts with:
  - **SMA** (Simple Moving Average)
  - **EMA** (Exponential Moving Average)
  - **RSI** (Relative Strength Index)
  - Optional **trendlines**
- Auto-refreshes based on user-selected interval.
- Timezone conversion support (default: `Asia/Kolkata`).
- Watchlist (`data/watchlist.csv`) with 50+ US stocks (S&P500 + Tech giants).
- Streamlit-based interactive dashboard.

---

## 📂 Project Structure
```
Stock Market Analysis/
│
├─ app/
│   └─ streamlit_app.py         # Main Streamlit dashboard
│
├─ data/
│   └─ watchlist.csv            # 50+ US stocks list
│
├─ src/
│   ├─ data_fetcher.py          # Functions to fetch data from Alpha Vantage
│   ├─ indicators.py            # SMA, EMA, RSI calculations
│   └─ plotting.py              # Plotly candlestick + trendline utilities
│
├─ venv/                        # Virtual environment (not pushed to GitHub)
├─ .env                         # Contains ALPHA_VANTAGE_API_KEY
├─ requirements.txt             # Dependencies
└─ README.md                    # Project documentation
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/stock-market-analysis.git
cd stock-market-analysis
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Linux/Mac
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure API Key
Create a `.env` file in the project root:
```
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

Get a free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).

### 5️⃣ Run the Streamlit App
```bash
streamlit run app/streamlit_app.py
```

---

## 📊 Example Dashboard

Features include candlestick chart, SMA/EMA overlays, RSI indicator, and auto-refresh intraday data.

---

## 📌 Future Enhancements
- Add **Top Gainers/Losers** dashboard from watchlist.
- Add support for **Indian markets** via `yfinance` or `nsetools`.
- Add user authentication for personalized watchlists.

---

## 🛠️ Tech Stack
- Python 3.10+
- Streamlit
- Plotly
- Pandas, Numpy
- Alpha Vantage API
