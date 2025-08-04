# bitget.py (ACTUALIZADO CON DATOS REALES)
import requests
import pandas as pd

def get_data():
    try:
        url_products = "https://api.bitget.com/api/spot/v1/public/products"
        url_prices = "https://api.bitget.com/api/spot/quote/v1/ticker/24hr"

        products = requests.get(url_products, timeout=10).json().get("data", [])
        prices = requests.get(url_prices, timeout=10).json().get("data", [])

        # Filtra productos spot activos
        spot_symbols = {
            item["symbolName"]: (item["baseCoin"], item["quoteCoin"])
            for item in products
            if item["status"] == "online" and item["symbolType"] == "_SPBL"
        }

        records = []
        for item in prices:
            symbol = item.get("symbol")
            if symbol in spot_symbols:
                base, quote = spot_symbols[symbol]
                bid = float(item.get("bestBid", 0))
                ask = float(item.get("bestAsk", 0))

                if bid > 0 and ask > 0:
                    records.append({
                        "base": base,
                        "quote": quote,
                        "bid": bid,
                        "ask": ask,
                        "exchange": "Bitget",
                        "link": f"https://www.bitget.com/spot/{symbol}"
                    })

        return pd.DataFrame(records)

    except Exception as e:
        print(f"💥 Error al obtener datos de Bitget: {e}")
        return pd.DataFrame(columns=["base", "quote", "bid", "ask", "exchange", "link"])
