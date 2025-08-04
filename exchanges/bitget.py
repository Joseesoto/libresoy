# exchanges/bitget.py

import requests
import pandas as pd

def get_data():
    url_products = "https://api.bitget.com/api/spot/v1/public/products"
    url_tickers = "https://api.bitget.com/api/spot/quote/v1/ticker/24hr"

    products = requests.get(url_products).json().get("data", [])
    tickers = requests.get(url_tickers).json().get("data", [])

    # Filtramos productos válidos
    symbol_map = {
        item["symbolName"]: item
        for item in products
        if item.get("status") == "online" and item.get("symbolType") == "_SPBL"
    }

    rows = []
    for ticker in tickers:
        symbol = ticker.get("symbol")
        product = symbol_map.get(symbol)
        if product:
            base = product.get("baseCoin")
            quote = product.get("quoteCoin")
            bid = float(ticker.get("bestBidPrice", 0))
            ask = float(ticker.get("bestAskPrice", 0))
            if bid > 0 and ask > 0:
                link = f"https://www.bitget.com/spot/{symbol}"
                rows.append({
                    "base": base,
                    "quote": quote,
                    "bid": bid,
                    "ask": ask,
                    "exchange": "Bitget",
                    "link": link
                })

    return pd.DataFrame(rows)
