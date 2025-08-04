import pandas as pd
import numpy as np

def get_all_data:
    pairs = [("BTC", "USDT"), ("ETH", "USDT"), ("SOL", "USDT"), ("XRP", "USDT"), ("ADA", "USDT"), ("XRP", "BTC")]
    data = []
    for base, quote in pairs:
        bid = round(np.random.uniform(100, 30000), 2)
        ask = round(bid + np.random.uniform(0.1, 1.5), 2)
        link = f"https://www.kucoin.com/trade/{base}-{quote}"
        data.append(["kucoin", base, quote, bid, ask, link])
    return pd.DataFrame(data, columns=["exchange", "base", "quote", "bid", "ask", "link"])
