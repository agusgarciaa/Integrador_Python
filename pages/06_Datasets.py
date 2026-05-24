# pages/06_Datasets.py
import streamlit as st
from src.exploraciones import generar_tabla_comparativa

st.set_page_config(page_title="Exploración - Datasets", layout="wide")

st.title("Exploración de Datasets")
st.markdown("Vista general y comparativa de todos los datasets disponibles en el sistema.")

st.header("Tabla comparativa de todos los datasets.")

df_comparativo = generar_tabla_comparativa()
if df_comparativo is not None:
    st.dataframe(df_comparativo, use_container_width=True)