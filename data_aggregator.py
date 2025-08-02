import pandas as pd
from exchanges import binance, kucoin, bybit, bitget

def get_mock_data():
    dfs = [
        binance.get_data(),
        kucoin.get_data(),
        bybit.get_data(),
        bitget.get_data()
    ]
    return pd.concat(dfs, ignore_index=True)
