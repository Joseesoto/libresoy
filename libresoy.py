import streamlit as st
import pandas as pd
from data_aggregator import get_mock_data

st.set_page_config(layout="wide")
st.title("🔍 Diagnóstico LibreSoy")

try:
    df = get_mock_data()
    st.success("✅ Datos cargados correctamente.")
    st.write("Columnas:", df.columns.tolist())
    st.write("Número de filas:", len(df))
    st.dataframe(df.head())
except Exception as e:
    st.error(f"❌ Error al cargar datos: {e}")
