# ============================================
# portfolio.py
# Buy/Sell stocks, track holdings and history
# ============================================

import json
import os
from datetime import datetime
from auth import load_users, save_users

# ── Buy a stock ──────────────────────────────
def buy_stock(username, stock, shares, buy_price):
    users = load_users()
    if username not in users:
        return False, "User not found!"

    record = {
        "id":        datetime.now().strftime("%Y%m%d%H%M%S"),
        "stock":     stock,
        "shares":    float(shares),
        "buy_price": float(buy_price),
        "date":      datetime.now().strftime("%Y-%m-%d"),
        "type":      "BUY"
    }

    users[username]["portfolio"].append(record)
    users[username]["history"].append(record)
    save_users(users)
    return True, f"Bought {shares} shares of {stock} at ${buy_price}"

# ── Sell a stock ─────────────────────────────
def sell_stock(username, record_id, sell_price):
    users = load_users()
    if username not in users:
        return False, "User not found!"

    portfolio = users[username]["portfolio"]
    for i, item in enumerate(portfolio):
        if item["id"] == record_id:
            profit = (float(sell_price) - item["buy_price"]) * item["shares"]
            sale = {
                "id":         record_id,
                "stock":      item["stock"],
                "shares":     item["shares"],
                "buy_price":  item["buy_price"],
                "sell_price": float(sell_price),
                "profit":     round(profit, 2),
                "date":       datetime.now().strftime("%Y-%m-%d"),
                "type":       "SELL"
            }
            users[username]["history"].append(sale)
            users[username]["portfolio"].pop(i)
            save_users(users)
            return True, f"Sold! Profit/Loss: ${profit:.2f}"

    return False, "Holding not found!"

# ── Get all holdings for a user ──────────────
def get_holdings(username):
    users = load_users()
    return users.get(username, {}).get("portfolio", [])

# ── Get transaction history for a user ───────
def get_history(username):
    users = load_users()
    return users.get(username, {}).get("history", [])