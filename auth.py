# ============================================
# auth.py
# User registration, login, password hashing
# ============================================

import json
import os
import hashlib

# Path to users file — same folder as this script
USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")

# ── Load all users ───────────────────────────
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            content = f.read().strip()
            return json.loads(content) if content else {}
    except:
        return {}

# ── Save all users ───────────────────────────
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# ── Hash password (SHA-256) ──────────────────
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ── Register new user ────────────────────────
def register_user(username, password):
    if not username or not password:
        return False, "Username and password required!"
    users = load_users()
    if username in users:
        return False, "Username already exists! Please choose another."
    users[username] = {
        "password":  hash_password(password),
        "portfolio": [],
        "history":   []
    }
    save_users(users)
    return True, f"Account created! Welcome {username} 🎉"

# ── Login user ───────────────────────────────
def login_user(username, password):
    if not username or not password:
        return False, "Please enter both username and password!"
    users = load_users()
    if username not in users:
        return False, "Username not found! Please register first."
    if users[username]["password"] != hash_password(password):
        return False, "Wrong password! Please try again."
    return True, f"Welcome back, {username}!"