import pandas as pd
import numpy as np

def get_data():
    pairs = [("BTC", "USDT"), ("ETH", "USDT"), ("SOL", "USDT"),  ("ADA", "USDT")]
    data = []
    for base, quote in pairs:
        bid = round(np.random.uniform(100, 30000), 2)
        ask = round(bid + np.random.uniform(0.1, 1.5), 2)
        link = f"https://www.bitget.com/en/spot/{base}{quote}"
        data.append(["Bitget", base, quote, f"{base}/{quote}", bid, ask, link])
    return pd.DataFrame(data, columns=["Exchange", "Base", "Quote", "Pair", "Bid", "Ask", "Link"])
