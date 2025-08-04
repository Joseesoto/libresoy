import streamlit as st
import pandas as pd
from data_aggregator import get_mock_data

st.set_page_config(layout="wide")
st.markdown("<h2 style='text-align: center;'>LibreSoy - Tabla SPOT</h2>", unsafe_allow_html=True)

# ------------------------
# Obtener y preparar datos
# ------------------------
df = get_mock_data()
df.columns = df.columns.str.lower().str.strip()  # Normaliza columnas

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

    if best_bid_row["bid"] <= 0 or best_ask_row["ask"] <= 0:
        continue

    spread = ((best_bid_row["bid"] - best_ask_row["ask"]) / best_ask_row["ask"]) * 100

    spreads_info.append({
        "pair": pair,
        "spread": spread,
        "buy_exchange": best_ask_row["exchange"],
        "buy_price": best_ask_row["ask"],
        "buy_link": best_ask_row["link"],
        "sell_exchange": best_bid_row["exchange"],
        "sell_price": best_bid_row["bid"],
        "sell_link": best_bid_row["link"],
        "group": group_sorted[["exchange", "bid", "ask", "link"]]
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
modo_compacto = st.toggle("Modo compacto", value=False)

if not spreads_info:
    st.warning("No hay resultados que cumplan con los filtros seleccionados.")
else:
    for s in spreads_info:
        st.markdown(f"""
            <div style='background-color:#f9f9f9; padding:12px; margin-top:20px; border-radius:10px;'>
                <div style='display:flex; justify-content:space-between; align-items:center; flex-wrap: wrap;'>
                    <span style='font-size:20px; font-weight:bold;'>Par: {s["pair"]}</span>
                </div>
        """, unsafe_allow_html=True)

        if modo_compacto:
            st.markdown(f"""
                <div style='margin-top:10px; display: flex; flex-direction:column; gap:10px;'>
                    <a href="{s["buy_link"]}" target="_blank" style='color:white; background-color:#006400; padding:8px 16px; border-radius:5px; text-align:center; text-decoration:none; font-weight:600;'>
                        🟢 Comprar en {s["buy_exchange"]} @ {s["buy_price"]:.{decimales}f}
                    </a>
                    <a href="{s["sell_link"]}" target="_blank" style='color:white; background-color:#b30000; padding:8px 16px; border-radius:5px; text-align:center; text-decoration:none; font-weight:600;'>
                        🔴 Vender en {s["sell_exchange"]} @ {s["sell_price"]:.{decimales}f}
                    </a>
                    <div style='text-align:center; font-size:16px; font-weight:600; color:#007bff;'>
                        Spread: {s["spread"]:.2f}%
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='margin-top:10px; display: flex; gap: 12px; flex-wrap: wrap; justify-content:space-between; align-items:center;'>
                    <a href="{s["buy_link"]}" target="_blank" style='flex: 1; color:white; background-color:#006400; padding:8px 16px; border-radius:5px; text-align:center; text-decoration:none; font-weight:600;'>
                        🟢 Comprar en {s["buy_exchange"]} @ {s["buy_price"]:.{decimales}f}
                    </a>
                    <span style='font-size:16px; font-weight:600; color:#007bff; flex: 0 0 auto; margin-left:12px;'>
                        Spread: {s["spread"]:.2f}%
                    </span>
                    <a href="{s["sell_link"]}" target="_blank" style='flex: 1; color:white; background-color:#b30000; padding:8px 16px; border-radius:5px; text-align:center; text-decoration:none; font-weight:600;'>
                        🔴 Vender en {s["sell_exchange"]} @ {s["sell_price"]:.{decimales}f}
                    </a>
                </div>
            """, unsafe_allow_html=True)

        # Tabla alineada justo debajo de los botones
        best_ask = s["group"]["ask"].min()
        best_bid = s["group"]["bid"].max()

        display_df = s["group"].copy()
        display_df.columns = ["exchange", "bid", "ask", "link"]

        display_df["bid"] = display_df["bid"].apply(
            lambda x: f"<span style='color:#006400; font-weight:bold'>{x:.{decimales}f}</span>" if x == best_bid else f"{x:.{decimales}f}"
        )
        display_df["ask"] = display_df["ask"].apply(
            lambda x: f"<span style='color:#b30000; font-weight:bold'>{x:.{decimales}f}</span>" if x == best_ask else f"{x:.{decimales}f}"
        )

        display_df["exchange"] = display_df.apply(
            lambda row: f"<a href='{row['link']}' target='_blank'>{row['exchange']}</a>", axis=1
        )
        display_df = display_df.drop(columns=["link"])

        st.markdown(
            f"""
            <div style='margin-top:10px; width: 100%; overflow-x: auto;'>
                {display_df.to_html(escape=False, index=False, classes="dataframe table table-striped", border=0)}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ------------------------
# Mostrar tabla completa (hasta 200 filas)
# ------------------------
st.dataframe(df.head(200), use_container_width=True)
