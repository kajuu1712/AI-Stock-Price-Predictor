# start.py — in ROOT folder
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard'))
from app import server