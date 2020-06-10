import json
import requests
import datetime

def stock_quote(symbol: str, token: str) -> dict:
    r = requests.get('https://finnhub.io/api/v1/quote?symbol={0}&token={1}').format(symbol, token)
    return r.json()

def stock_splits():
    return 1