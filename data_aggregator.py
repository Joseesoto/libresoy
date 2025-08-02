import pandas as pd
from sources import binance, kucoin, bybit, bitget  # Asegúrate que estos módulos estén bien importados

def get_mock_data():
    required_cols = ["base", "quote", "bid", "ask", "exchange", "link"]

    sources = {
        "Binance": binance.get_data,
        "KuCoin": kucoin.get_data,
        "Bybit": bybit.get_data,
        "Bitget": bitget.get_data
    }

    valid_dfs = []

    for name, get_data_func in sources.items():
        print(f"\n🔍 Procesando {name}")
        try:
            df = get_data_func()
            if isinstance(df, pd.DataFrame):
                df.columns = df.columns.str.lower().str.strip()  # Normaliza nombres
                missing = set(required_cols) - set(df.columns)
                if not missing:
                    print(f"✅ {name}: columnas válidas ({len(df)} filas)")
                    valid_dfs.append(df)
                else:
                    print(f"⚠️ {name} omitido: columnas faltantes {missing}")
            else:
                print(f"❌ {name} no devolvió un DataFrame válido")
        except Exception as e:
            print(f"💥 Error en {name}: {e}")

    if not valid_dfs:
        print("\n🚫 Ningún módulo pasó la validación")
        return pd.DataFrame(columns=required_cols)

    print(f"\n📊 Total de filas combinadas: {sum(len(df) for df in valid_dfs)}")
    return pd.concat(valid_dfs, ignore_index=True)
