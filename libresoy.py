import streamlit as st
import pandas as pd
from data_aggregator import get_mock_data

st.set_page_config(layout="wide")
st.markdown("""
    <style>
        body {
            font-family: "Segoe UI", sans-serif;
        }
        .panel {
            background-color: #f9f9f9;
            padding: 20px;
            margin-top: 30px;
            border-radius: 12px;
            max-width: 960px;
            margin-left: auto;
            margin-right: auto;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        .title {
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 6px;
        }
        .spread {
            text-align: center;
            font-size: 16px;
            font-weight: 600;
            color: #007bff;
            margin-bottom: 16px;
        }
        .buttons {
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 16px;
        }
        .btn {
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            color: white;
            text-align: center;
            display: inline-block;
        }
        .buy { background-color: #006400; }
        .sell { background-color: #b30000; }
        .table-wrapper {
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }
        th {
            background-color: #eaeaea;
            text-align: center;
            padding: 8px;
        }
        td {
            text-align: center;
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>LibreSoy - Tabla SPOT</h2>", unsafe_allow_html=True)

# ------------------------
# Obtener y preparar datos
# ------------------------
df = get_mock_data()
df.columns = df.columns.str.lower().str.strip()

if df.empty:
    st.error("❌ El DataFrame está vacío. Revisa los módulos de los exchanges.")
    st.stop()

required_cols = {"base", "quote", "bid", "ask", "exchange", "link"}
missing = required_cols - set(df.columns)

if missing:
    st.error(f"❌ Faltan columnas: {', '.join(missing)}")
    st.stop()

df["pair"] = df["base"] + "/" + df["quote"]

# ------------------------
# Sidebar - Filtros
# ------------------------
with st.sidebar:
    st.markdown("## Filtros")

    exchange_opts = sorted(df["exchange"].unique())
    base_opts = sorted(set(df["base"].unique()) | set(df["quote"].unique()))
    quote_opts = sorted(df["quote"].unique())

    selected_exchanges = st.multiselect("Exchange", exchange_opts, default=exchange_opts)
    selected_base = st.selectbox("Base", ["Todos"] + base_opts)
    selected_quotes = st.multiselect("Quote", quote_opts, default=quote_opts)
    decimales = st.slider("Decimales a mostrar", min_value=2, max_value=6, value=4)

# Filtrar por exchange, base y quote
df = df[df["exchange"].isin(selected_exchanges)]
if selected_base != "Todos":
    df = df[(df["base"] == selected_base) | (df["quote"] == selected_base)]
if selected_quotes:
    df = df[df["quote"].isin(selected_quotes)]

# ------------------------
# Agrupar y calcular spreads
# ------------------------
spreads_info = []

for pair, group in df.groupby("pair"):
    group_sorted = group.sort_values(["ask", "bid"])

    best_ask_row = group_sorted.loc[group_sorted["ask"].idxmin()]
    best_bid_row = group_sorted.loc[group_sorted["bid"].idxmax()]

    if best_bid_row["bid"] <=
