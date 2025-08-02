def get_mock_data():
    sources = {
        "Binance": binance.get_data(),
        "KuCoin": kucoin.get_data(),
        "Bybit": bybit.get_data(),
        "Bitget": bitget.get_data()
    }

    valid_dfs = []

    for name, df in sources.items():
        if isinstance(df, pd.DataFrame):
            required_cols = {"base", "quote", "bid", "ask", "exchange", "link"}
            if required_cols.issubset(df.columns):
                valid_dfs.append(df)
            else:
                print(f"⚠️ {name} omitido: columnas faltantes {required_cols - set(df.columns)}")
        else:
            print(f"⚠️ {name} omitido: no devolvió un DataFrame válido")

    if not valid_dfs:
        return pd.DataFrame(columns=list(required_cols))

    return pd.concat(valid_dfs, ignore_index=True)
