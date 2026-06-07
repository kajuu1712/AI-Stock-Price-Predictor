# 📈 AI-Based Stock Price Predictor

A machine learning project that predicts stock prices using historical data analysis and provides an interactive visualization dashboard with technical indicators.

**Internship Project | 2026**

---

## 🌐 Live Demo

**Dashboard Link:**
[Open Dashboard](https://ai-stock-price-predictor-6qc4.onrender.com/)

---

## 🎯 Project Overview

This project uses historical stock market data to build a machine learning model that predicts stock closing prices and provides an interactive dashboard for visualization and analysis.

The dashboard supports multiple stocks and allows users to explore historical trends, model predictions, trading volume, volatility, yearly price distributions, and technical indicators (RSI & MACD).

---

## 🚀 How to Run This Project Locally

### Step 1 — Clone the Repository
```bash
git clone <your-github-repository-url>
cd stock-predictor
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run the Dashboard
```bash
python app.py
```

### Step 4 — Open in Browser
```
http://localhost:8050
```

The dashboard will automatically download stock data from Yahoo Finance and display interactive charts.

---

## 📊 Project Workflow

```
Step 1: Data Collection
    └── Download historical stock data using yfinance

Step 2: Data Exploration (EDA)
    └── Analyze stock trends, visualize patterns, study volatility,
        check statistics and understand the dataset before ML

Step 3: Data Preprocessing
    └── Clean missing values, scale data, create useful features
        (Moving Averages, Daily Range, RSI, MACD etc.),
        and prepare the dataset for machine learning

Step 4: Model Building
    └── Train Linear Regression model to predict closing prices
    └── Evaluate using MAE and R² Score (achieved 99.99% accuracy)

Step 5: Visualization
    └── Plot actual vs predicted prices
    └── Create interactive charts using Plotly

Step 6: Dashboard
    └── Multi-stock Dash web application
    └── Interactive visualizations and prediction lookup
    └── RSI and MACD technical indicator charts
```

---

## 📈 Supported Stocks

| Company | Ticker |
|---------|--------|
| Apple Inc. | AAPL |
| Microsoft | MSFT |
| Google (Alphabet) | GOOGL |
| Reliance Industries | RELIANCE.NS |
| Tata Consultancy Services | TCS.NS |

---

## 📊 Dashboard Features

- 📈 Historical Price Chart with 50-Day & 200-Day Moving Averages
- 🤖 Actual vs Predicted Price Comparison
- ⚡ RSI (Relative Strength Index) with Overbought/Oversold zones
- 📉 MACD with Signal Line and momentum Histogram
- 📊 Trading Volume Analysis
- 📏 Daily Volatility (High − Low Range)
- 📅 Yearly Price Distribution Box Plots
- 🔮 Date-wise Prediction Viewer with RSI Signal
- 📌 Multi-Stock Selection Support

---

## 📉 Model Performance

| Metric | Value | Meaning |
|--------|-------|---------|
| R² Score | 99.99% | Model explains 99.99% of price variation |
| MAE | $0.47 | Average prediction error of 47 cents |
| RMSE | $0.75 | Even large errors stay under $1 |
| Features Used | 10 | Open, High, Low, Volume, MA_50, MA_200, Daily_Range, RSI, MACD, MACD_Signal |

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.11 |
| Data Collection | yfinance |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn (Linear Regression) |
| Technical Indicators | RSI, MACD (custom implementation) |
| Visualization | Matplotlib, Seaborn, Plotly |
| Dashboard | Dash |
| Deployment | Render.com + Gunicorn |

---

## ☁️ Deployment

The dashboard is deployed on **Render** (free tier) and can be accessed directly through the live link above.

Deployment uses:
- **Gunicorn** as the production web server
- **render.yaml** for automatic configuration
- **GitHub** for continuous deployment (auto-deploys on every push)

---

## 🔮 Future Enhancements


### Priority 1 — User Management & Portfolio Tracker 
**What:** Allow users to register/login and manage their personal stock portfolio.
Users can record buy/sell transactions, track profit/loss in real time,
and receive smart Hold/Buy/Sell signals powered by RSI and MACD.

**Why important:** Transforms the dashboard from a read-only tool into
a fully interactive personal finance application. Directly applies
the RSI and MACD indicators already built into the system.

**Features planned:**
- User registration and login
- Buy stocks (enter stock, quantity, price, date)
- Live portfolio tracking (current value, profit/loss %)
- Smart signals: RSI + MACD based Hold/Buy/Sell recommendations
- Full transaction history

---

### Priority 2 — Stock Comparison Dashboard
**What:** Show two or more stocks side by side in the same chart
for easy visual comparison of price trends, RSI, and MACD.

**Why important:** Investors always compare stocks before deciding
where to invest. This adds significant analytical value to the dashboard
and is a highly requested feature in financial tools.

**Features planned:**
- Select 2 stocks simultaneously
- Overlay price charts with normalized scale
- Compare RSI and MACD side by side
- Show correlation between selected stocks

---

### Priority 3 — LSTM Deep Learning Model
**What:** Replace or complement the Linear Regression model with an
LSTM (Long Short-Term Memory) neural network, which is specifically
designed for time series and sequential data like stock prices.

**Why important:** LSTM can capture long-term patterns and dependencies
in stock data that Linear Regression cannot. It is the industry standard
model used by quantitative finance teams and hedge funds for price prediction.

**Features planned:**
- Build LSTM model using TensorFlow/Keras
- Compare LSTM vs Linear Regression accuracy
- Allow user to switch between models on dashboard
- Show prediction confidence intervals

---

### Priority 4 — Real-Time Stock Data Streaming
**What:** Fetch live intraday stock prices and update charts
automatically every few minutes without page refresh.

**Why important:** Currently the dashboard uses historical end-of-day data.
Real-time streaming would make it usable for actual trading decisions
during market hours.

**Features planned:**
- WebSocket or polling-based live price updates
- Intraday charts (minute-by-minute)
- Live RSI and MACD updates
- Price alerts (notify when RSI crosses 70 or 30)

---

### Priority 5 — News Sentiment Analysis
**What:** Fetch recent news headlines about a stock and use
Natural Language Processing (NLP) to determine if the sentiment
is positive, negative, or neutral — then factor this into predictions.

**Why important:** Stock prices are heavily influenced by news events.
A model that combines historical price patterns with current news
sentiment would be significantly more accurate during volatile periods.

**Features planned:**
- Fetch news from financial APIs
- Sentiment scoring using NLP (positive/negative/neutral)
- Sentiment score as additional ML feature
- News feed displayed on dashboard

---

### Priority 6 — Portfolio Performance Analytics
**What:** Advanced analytics for the portfolio tracker including
risk metrics, Sharpe ratio, diversification score, and performance
comparison against market benchmarks like S&P 500.

**Why important:** Professional investors don't just track profit —
they track risk-adjusted returns. This would make the tool suitable
for serious investors and financial analysis coursework.

**Features planned:**
- Sharpe ratio calculation
- Portfolio diversification analysis
- Benchmark comparison (vs S&P 500, Nifty 50)
- Monthly/yearly performance reports

---

## 👩‍💻 Author

**Kajal**
Internship Project — 2026

---

## 📚 References

- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Plotly Dash Documentation](https://dash.plotly.com/)
- [RSI — Investopedia](https://www.investopedia.com/terms/r/rsi.asp)
- [MACD — Investopedia](https://www.investopedia.com/terms/m/macd.asp)
- [Yahoo Finance — AAPL](https://finance.yahoo.com/quote/AAPL)