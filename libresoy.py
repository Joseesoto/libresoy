import streamlit as st
import pandas as pd
from mock_data import get_all_data

st.set_page_config(page_title="LibreSoy - Comparador de Exchanges", layout="wide")

st.markdown("""
    <style>
    .highlight-bid {color: green; font-weight: bold;}
    .highlight-ask {color: red; font-weight: bold;}
    .exchange-link {text-decoration: none; color: #3366cc; font-weight: bold;}
    .custom-button {display: inline-block; margin-right: 10px; margin-bottom: 10px; padding: 0.5em 1em; border-radius: 8px; text-decoration: none;}
    .buy-button {background-color: #ff4d4d; color: white;}
    .sell-button {background-color: #2ecc71; color: white;}
    </style>
""", unsafe_allow_html=True)

st.title("🔄 LibreSoy - Comparador de Exchanges")

df = get_all_data()

# Sidebar filters
exchanges = st.sidebar.multiselect("Filtrar por Exchange", sorted(df["exchange"].unique()), default=sorted(df["exchange"].unique()))
bases = st.sidebar.multiselect("Filtrar por Moneda Base", sorted(df["base"].unique()), default=sorted(df["base"].unique()))
quotes = st.sidebar.multiselect("Filtrar por Moneda Cotizada", sorted(df["quote"].unique()), default=sorted(df["quote"].unique()))
spread_limit = st.sidebar.number_input("Máximo Spread (%)", value=100.0, step=0.1)
decimals = st.sidebar.slider("Número de decimales", 2, 6, 4)

# Aplicar filtros
df_filtered = df[df["exchange"].isin(exchanges)]
df_filtered = df_filtered[df_filtered["base"].isin(bases)]
df_filtered = df_filtered[df_filtered["quote"].isin(quotes)]
df_filtered["base_quote"] = df_filtered["base"] + "/" + df_filtered["quote"]

# Calcular mejores precios por par
best_bids = df_filtered.loc[df_filtered.groupby("base_quote")["bid"].idxmax()]
best_asks = df_filtered.loc[df_filtered.groupby("base_quote")["ask"].idxmin()]

# Calcular spreads
merged = pd.merge(best_bids, best_asks, on="base_quote", suffixes=("_bid", "_ask"))
merged["spread"] = ((merged["ask_ask"] - merged["bid_bid"]) / merged["bid_bid"]) * 100
merged = merged[merged["spread"] <= spread_limit]

# Mostrar resultados
for _, row in merged.iterrows():
    st.markdown(f"### {row['base_quote']} - Spread: {row['spread']:.2f}%")

    buy_btn = f"""
    <a href="{row['link_bid']}" target="_blank" class="custom-button buy-button">
        Comprar en {row['exchange_bid']} @ {row['bid_bid']:.{decimals}f}
    </a>
    """
    sell_btn = f"""
    <a href="{row['link_ask']}" target="_blank" class="custom-button sell-button">
        Vender en {row['exchange_ask']} @ {row['ask_ask']:.{decimals}f}
    </a>
    """
    st.markdown(buy_btn + sell_btn, unsafe_allow_html=True)

    pair_df = df_filtered[df_filtered["base_quote"] == row["base_quote"]].copy()
    pair_df["Exchange"] = pair_df.apply(lambda x: f'<a href="{x["link"]}" target="_blank" class="exchange-link">{x["exchange"]}</a>', axis=1)
    pair_df["Bid"] = pair_df["bid"].apply(lambda x: f'<span class="highlight-bid">{x:.{decimals}f}</span>' if x == row["bid_bid"] else f"{x:.{decimals}f}")
    pair_df["Ask"] = pair_df["ask"].apply(lambda x: f'<span class="highlight-ask">{x:.{decimals}f}</span>' if x == row["ask_ask"] else f"{x:.{decimals}f}")
    
    st.markdown(pair_df[["Exchange", "Bid", "Ask"]].to_html(escape=False, index=False), unsafe_allow_html=True)
    st.markdown("---")
