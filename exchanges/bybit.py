# exchanges/bybit.py

import requests
import pandas as pd

def get_data():
    try:
        url_info = "https://api.bybit.com/v5/market/instruments-info?category=spot"
        url_prices = "https://api.bybit.com/v5/market/tickers?category=spot"

        products = requests.get(url_info, timeout=10).json().get("result", {}).get("list", [])
        tickers = requests.get(url_prices, timeout=10).json().get("result", {}).get("list", [])

        activos = {item["symbol"]: item for item in products if item["status"] == "Trading"}

        data = []
        for ticker in tickers:
            symbol = ticker.get("symbol", "")
            if symbol in activos:
                info = activos[symbol]
                base = info["baseCoin"]
                quote = info["quoteCoin"]
                bid = ticker.get("bid1Price", "0")
                ask = ticker.get("ask1Price", "0")

                if float(bid) > 0 and float(ask) > 0:
                    link = f"https://www.bybit.com/trade/spot/{base}/{quote}"
                    data.append({
                        "base": base,
                        "quote": quote,
                        "bid": float(bid),
                        "ask": float(ask),
                        "exchange": "Bybit",
                        "link": link
                    })

        return pd.DataFrame(data)

    except Exception as e:
        print(f"💥 Error al obtener datos de Bybit: {e}")
        return pd.DataFrame(columns=["base", "quote", "bid", "ask", "exchange", "link"])
