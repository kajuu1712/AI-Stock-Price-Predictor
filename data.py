# ============================================
# data.py
# All stock data downloading and ML functions
# ============================================

import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

# ── Supported Stocks ─────────────────────────
STOCKS = {
    'AAPL':        'Apple Inc.',
    'RELIANCE.NS': 'Reliance Industries',
    'TCS.NS':      'Tata Consultancy Services',
    'GOOGL':       'Google (Alphabet)',
    'MSFT':        'Microsoft',
}

# ── RSI Calculation ──────────────────────────
def calculate_rsi(series, period=14):
    delta    = series.diff()
    gain     = delta.clip(lower=0)
    loss     = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs       = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# ── MACD Calculation ─────────────────────────
def calculate_macd(series, fast=12, slow=26, signal=9):
    ema_fast    = series.ewm(span=fast,   adjust=False).mean()
    ema_slow    = series.ewm(span=slow,   adjust=False).mean()
    macd_line   = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram   = macd_line - signal_line
    return macd_line, signal_line, histogram

# ── Download + Train for any Stock ───────────
def get_stock_data(ticker):
    print(f"Downloading: {ticker}")
    df = yf.download(
        ticker,
        period="10y",
        progress=False,
        threads=False,
        auto_adjust=True,
        actions=False
    )

    if df.empty:
        raise Exception(f"No data for {ticker}")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    required = ['Open', 'High', 'Low', 'Close', 'Volume']
    missing  = [c for c in required if c not in df.columns]
    if missing:
        raise Exception(f"Missing columns: {missing}")

    df = df[required].copy()
    df.index = pd.to_datetime(df.index)

    df['MA_50']       = df['Close'].rolling(50).mean()
    df['MA_200']      = df['Close'].rolling(200).mean()
    df['Daily_Range'] = df['High'] - df['Low']
    df['Year']        = df.index.year
    df['RSI']         = calculate_rsi(df['Close'])
    df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = calculate_macd(df['Close'])
    df = df.dropna()

    if len(df) == 0:
        raise Exception("No data after processing")

    features = ['Open','High','Low','Volume',
                'MA_50','MA_200','Daily_Range',
                'RSI','MACD','MACD_Signal']

    X        = df[features]
    y        = df['Close']
    scaler   = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    model    = LinearRegression()
    model.fit(X_scaled, y)
    df['Predicted'] = model.predict(X_scaled)

    r2  = round(r2_score(y, df['Predicted']) * 100, 2)
    mae = round(mean_absolute_error(y, df['Predicted']), 2)
    print(f"Done! R²={r2}%, MAE=${mae}")
    return df, r2, mae

# ── Get Latest Price Only ────────────────────
def get_latest_price(ticker):
    try:
        df = yf.download(
            ticker,
            period="5d",
            progress=False,
            threads=False,
            auto_adjust=True,
            actions=False
        )
        if df.empty:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return round(float(df['Close'].iloc[-1]), 2)
    except:
        return None

# ── Get RSI + MACD Signal for a Stock ────────
def get_trade_signal(ticker):
    """Returns (rsi_value, rsi_signal, macd_signal)"""
    try:
        df, _, _ = get_stock_data(ticker)
        rsi      = round(float(df['RSI'].iloc[-1]), 1)
        macd_val = float(df['MACD'].iloc[-1])
        macd_sig = float(df['MACD_Signal'].iloc[-1])

        if rsi > 70:
            rsi_signal = "🔴 SELL — Overbought"
        elif rsi < 30:
            rsi_signal = "🟢 BUY — Oversold"
        else:
            rsi_signal = "🟡 HOLD — Neutral"

        macd_signal = "📈 Bullish" if macd_val > macd_sig else "📉 Bearish"
        return rsi, rsi_signal, macd_signal
    except:
        return 0, "N/A", "N/A"