# 📈 AI-Based Stock Price Predictor

A machine learning project that predicts stock prices using historical data analysis and provides an interactive visualization dashboard.

---

## 🎯 Project Overview

This project uses historical stock market data of **Apple Inc. (AAPL)** to build a machine learning model that predicts future stock prices. It includes data collection, preprocessing, model training, evaluation, and an interactive dashboard for visualization.

**Internship Project | 2026**

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.13 |
| Data Collection | yfinance |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Visualization | Matplotlib, Seaborn, Plotly |
| Dashboard | Dash |
| Environment | Jupyter Notebook, VS Code |

---

## 📁 Folder Structure

```
stock-predictor/
│
├── data/
│   ├── raw/                  # Raw stock data downloaded from yfinance
│   └── processed/            # Cleaned and feature-engineered data
│
├── notebooks/
│   ├── 01_data_collection.ipynb      # Fetch stock data using yfinance
│   ├── 02_data_exploration.ipynb     # EDA - charts, trends, statistics
│   ├── 03_data_preprocessing.ipynb   # Cleaning, feature engineering
│   ├── 04_model_building.ipynb       # Train ML model, evaluate accuracy
│   └── 05_visualization.ipynb        # Final charts and visual insights
│
├── src/
│   ├── data_loader.py        # Functions to fetch and save stock data
│   ├── preprocessor.py       # Data cleaning and feature engineering
│   ├── model.py              # ML model training and prediction
│   └── visualizer.py         # Reusable chart functions
│
├── dashboard/
│   └── app.py                # Interactive Dash web dashboard
│
├── models/
│   └── stock_model.pkl       # Saved trained ML model
│
├── docs/
│   └── project_report.pdf    # Final project report
│
├── requirements.txt           # All Python dependencies
├── .gitignore
└── README.md                  # Project documentation (this file)
```

---

## 🚀 How to Run This Project

### Step 1 — Clone or Download the Project
```bash
cd Desktop
cd stock-predictor
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Launch Jupyter Notebook
```bash
cd notebooks
jupyter notebook
```

### Step 4 — Run Notebooks in Order
```
01_data_collection.ipynb      ← Start here
02_data_exploration.ipynb
03_data_preprocessing.ipynb
04_model_building.ipynb
05_visualization.ipynb
```

### Step 5 — Run the Dashboard
```bash
cd dashboard
python app.py
```
Then open your browser and go to: `http://localhost:8050`

---

## 📊 Project Workflow

```
Step 1: Data Collection
    └── Download AAPL historical data (2015–2024) using yfinance

Step 2: Data Exploration (EDA)
    └── Analyze stock trends, visualize patterns, study volatility,
        check statistics and understand the dataset before ML

Step 3: Data Preprocessing
    └── Clean missing values, scale data, create useful features
        (Moving Averages, Daily Range, RSI, etc.), and prepare
        the dataset for machine learning

Step 4: Model Building
    └── Train Linear Regression model to predict closing prices
    └── Evaluate using MAE, RMSE, R² Score

Step 5: Visualization
    └── Plot actual vs predicted prices
    └── Interactive charts using Plotly

Step 6: Dashboard
    └── Dash web app showing live predictions and charts
```

---

## 📈 Stock Details

| Detail | Info |
|--------|------|
| Stock | Apple Inc. |
| Ticker Symbol | AAPL |
| Data Source | Yahoo Finance (via yfinance) |
| Historical Range | 2015 – 2024 |
| Prediction Target | Closing Price |

---

## 🤖 Machine Learning Model

| Detail | Info |
|--------|------|
| Algorithm | Linear Regression |
| Library | Scikit-learn |
| Features Used | Open, High, Low, Volume, Moving Averages |
| Target Variable | Close Price (next day) |
| Evaluation Metrics | MAE, RMSE, R² Score |

---

## 📉 Evaluation Metrics Explained

- **MAE (Mean Absolute Error)** — Average error in price prediction (lower is better)
- **RMSE (Root Mean Squared Error)** — Penalizes large errors more (lower is better)
- **R² Score** — How well the model fits the data (closer to 1.0 is better)

---

## 🔮 Future Improvements

- [ ] Add LSTM (Deep Learning) model for better accuracy
- [ ] Predict multiple stocks simultaneously
- [ ] Add live/real-time stock price fetching
- [ ] Deploy dashboard to web (Heroku / Render)
- [ ] Add news sentiment analysis for better predictions

---

## 👩‍💻 Author

**Kajal**
Internship Project — 2026

---

## 📚 References

- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Plotly Dash Documentation](https://dash.plotly.com/)
- [Yahoo Finance — AAPL](https://finance.yahoo.com/quote/AAPL)