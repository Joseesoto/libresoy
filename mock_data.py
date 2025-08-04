import pandas as pd
from Exchanges.binance_spot import fetch_binance
from Exchanges.kucoin_spot import fetch_kucoin
from Exchanges.bybit_spot import fetch_bybit
from Exchanges.bitget_spot import fetch_bitget

def get_all_data():
    all_data = []

    sources = {
        "Binance": fetch_binance,
        "KuCoin": fetch_kucoin,
        "Bybit": fetch_bybit,
        "Bitget": fetch_bitget
    }

    for name, func in sources.items():
        try:
            df = func()
            if df is not None and not df.empty and all(col in df.columns for col in ["base", "quote", "bid", "ask", "exchange", "link"]):
                all_data.append(df)
            else:
                print(f"⚠️ {name}: DataFrame inválido o columnas incompletas.")
        except Exception as e:
            print(f"❌ Error al obtener datos de {name}: {e}")

    if not all_data:
        return pd.DataFrame(columns=["base", "quote", "bid", "ask", "exchange", "link"])

    combined = pd.concat(all_data, ignore_index=True)
    combined = combined[(combined["bid"] > 0) & (combined["ask"] > 0)]
    return combined
