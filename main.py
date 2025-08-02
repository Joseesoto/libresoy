import streamlit as st
import pandas as pd

st.set_page_config(page_title="LibreSoy SPOT", layout="wide")

st.title("📊 LibreSoy - Visualizador SPOT")
st.markdown("Visualiza oportunidades de arbitraje entre exchanges en tiempo real.")

# Simulación de datos
data = pd.DataFrame({
    "Pair": ["BTC/USDT", "ETH/USDT", "SOL/USDT"],
    "Exchange A": [29100, 1850, 24.5],
    "Exchange B": [29050, 1845, 24.8],
    "Spread (%)": [0.17, 0.27, -1.22]
})

st.dataframe(data, use_container_width=True)
