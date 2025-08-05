# exchanges/bybit.py

import pandas as pd
import requests

def get_data():
    try:
        # Obtener lista de símbolos spot
        symbols_url = "https://api.bybit.com/v5/market/instruments?category=spot"
        symbols_resp = requests.get(symbols_url, timeout=10)
        symbols = symbols_resp.json().get("result", {}).get("list", [])

        # Obtener precios de ticker
        ticker_url = "https://api.bybit.com/v5/market/tickers?category=spot"
        ticker_resp = requests.get(ticker_url, timeout=10)
        tickers = ticker_resp.json().get("result", {}).get("list", [])

        # Filtrar tickers con precios válidos y construir DataFrame
        data = []
        ticker_map = {t['symbol']: t for t in tickers}

        for s in symbols:
            symbol = s.get("symbol")
            base = s.get("baseCoin")
            quote = s.get("quoteCoin")

            t = ticker_map.get(symbol)
            if not t:
                continue

            bid = float(t.get("bid1Price", 0))
            ask = float(t.get("ask1Price", 0))

            if bid > 0 and ask > 0:
                data.append({
                    "base": base,
                    "quote": quote,
                    "bid": bid,
                    "ask": ask,
                    "exchange": "Bybit",
                    "link": f"https://www.bybit.com/en/trade/spot/{base}/{quote}"
                })

        return pd.DataFrame(data)

    except Exception as e:
        print(f"💥 Error al obtener datos de Bybit: {e}")
        return pd.DataFrame(columns=["base", "quote", "bid", "ask", "exchange", "link"])
