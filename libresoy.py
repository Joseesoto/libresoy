import streamlit as st
import pandas as pd
from data_aggregator import get_mock_data

st.set_page_config(layout="wide")
st.markdown("<h2 style='text-align: center;'>LibreSoy - Tabla SPOT</h2>", unsafe_allow_html=True)

# ------------------------
# Obtener y preparar datos
# ------------------------
df = get_mock_data()
# Validar columnas antes de crear 'pair'
required_cols = {"base", "quote"}
missing = required_cols - set(df.columns)

if not missing:
    df["pair"] = df["base"] + "/" + df["quote"]
else:
    st.error(f"❌ Faltan las columnas necesarias: {', '.join(missing)}. Revisa la función get_mock_data().")
    st.stop()

df["pair"] = df["base"] + "/" + df["quote"]

# ------------------------
# Sidebar - Filtros
# ------------------------
with st.sidebar:
    st.markdown("## Filtros")

    exchange_opts = sorted(df["Exchange"].unique())
    base_opts = sorted(set(df["base"].unique()) | set(df["quote"].unique()))
    quote_opts = sorted(df["quote"].unique())

    selected_exchanges = st.multiselect("Exchange", exchange_opts, default=exchange_opts)
    selected_base = st.selectbox("Base", ["Todos"] + base_opts)
    selected_quotes = st.multiselect("Quote", quote_opts, default=quote_opts)
    decimales = st.slider("Decimales a mostrar", min_value=2, max_value=6, value=4)

# Filtrar por exchange, base y quote
df = df[df["Exchange"].isin(selected_exchanges)]
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

    if best_bid_row["bid"] <= 0 or best_ask_row["ask"] <= 0:
        continue

    spread = ((best_bid_row["bid"] - best_ask_row["ask"]) / best_ask_row["ask"]) * 100

    spreads_info.append({
        "pair": pair,
        "spread": spread,
        "buy_exchange": best_ask_row["Exchange"],
        "buy_price": best_ask_row["ask"],
        "buy_link": best_ask_row["link"],
        "sell_exchange": best_bid_row["Exchange"],
        "sell_price": best_bid_row["bid"],
        "sell_link": best_bid_row["link"],
        "group": group_sorted[["Exchange", "bid", "ask", "link"]]
    })

# ------------------------
# Filtro adicional por Spread
# ------------------------
if spreads_info:
    min_spread = min(s["spread"] for s in spreads_info)
    max_spread = max(s["spread"] for s in spreads_info)

    with st.sidebar:
        spread_range = st.slider("Rango de Spread (%)",
                                 min_value=round(min_spread, 2),
                                 max_value=round(max_spread, 2),
                                 value=(round(min_spread, 2), round(max_spread, 2)))

    spreads_info = [s for s in spreads_info if spread_range[0] <= s["spread"] <= spread_range[1]]

# ------------------------
# Mostrar resultados
# ------------------------
st.markdown("### Resultados:")

if not spreads_info:
    st.warning("No hay resultados que cumplan con los filtros seleccionados.")
else:
    for s in spreads_info:
        st.markdown(f"""
            <div style='background-color:#f9f9f9; padding:12px; margin-top:20px; border-radius:10px;'>
                <div style='display:flex; justify-content:space-between; align-items:center; flex-wrap: wrap;'>
                    <span style='font-size:20px; font-weight:bold;'>Par: {s["pair"]}</span>
                    <span style='font-size:16px;'><b>Spread:</b> {s["spread"]:.2f}%</span>
                </div>
                <div style='margin-top:10px; display: flex; gap: 12px; flex-wrap: wrap;'>
                    <a href="{s["buy_link"]}" target="_blank" style='flex: 0 0 auto; color:white; background-color:#218838; padding:6px 16px; border-radius:5px; text-decoration:none; font-weight:600;'>
                        Comprar en {s["buy_exchange"]} @ {s["buy_price"]:.{decimales}f}
                    </a>
                    <a href="{s["sell_link"]}" target="_blank" style='flex: 0 0 auto; color:white; background-color:#c82333; padding:6px 16px; border-radius:5px; text-decoration:none; font-weight:600;'>
                        Vender en {s["sell_exchange"]} @ {s["sell_price"]:.{decimales}f}
                    </a>
                </div>
            </div>
        """, unsafe_allow_html=True)

        display_df = s["group"].copy()
        display_df.columns = ["Exchange", "Precio Venta (Bid)", "Precio Compra (Ask)", "Link"]

        # Formatear precios con decimales
        display_df["Precio Venta (Bid)"] = display_df["Precio Venta (Bid)"].apply(lambda x: f"<span style='color:#006400; font-weight:bold'>{x:.{decimales}f}</span>")
        display_df["Precio Compra (Ask)"] = display_df["Precio Compra (Ask)"].apply(lambda x: f"<span style='color:#b30000; font-weight:bold'>{x:.{decimales}f}</span>")

        # Convertir nombre de Exchange en un enlace
        display_df["Exchange"] = display_df.apply(lambda row: f"<a href='{row['Link']}' target='_blank'>{row['Exchange']}</a>", axis=1)
        display_df = display_df.drop(columns=["Link"])

        # Mostrar tabla alineada con botones
        st.markdown(
            f"""
            <div style='margin-top:-10px; max-width: 900px;'>
                {display_df.to_html(escape=False, index=False, classes="dataframe table table-striped", border=0)}
            </div>
            """,
            unsafe_allow_html=True
        )
st.write("✅ Datos cargados:")
st.dataframe(df)
