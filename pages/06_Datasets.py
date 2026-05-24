# pages/06_Datasets.py
import os
import src.file_manager as fm
import streamlit as st
from src.exploraciones import generar_tabla_comparativa

st.set_page_config(page_title="Exploración - Datasets", layout="wide")

st.title("Exploración de Datasets")
st.markdown("Vista general y comparativa de todos los datasets disponibles en el sistema.")

st.header("Tabla comparativa de todos los datasets.")

df_comparativo = generar_tabla_comparativa()
if df_comparativo is not None:
    st.dataframe(df_comparativo, use_container_width=True)
   
ruta = fm.obtener_raiz_proyecto() 
ruta_dataset1=ruta / "documentation" / "dataset_a1.md"
ruta_dataset2=ruta / "documentation" / "dataset_a2.md"
ruta_dataset3=ruta / "documentation" / "dataset_a3.md"

documento=st.selectbox("seleccione el documento markdown que quiere visualizar",["dataset1","dataset2","dataset3"])
if documento:
    if documento=="dataset1":
        ruta=ruta_dataset1
    elif documento=="dataset2":
        ruta=ruta_dataset2
    elif documento=="dataset3":
        ruta=ruta_dataset3
    if os.path.exists(ruta):
        with open(ruta,encoding="utf-8") as archivo:
            markdown=archivo.read()
            st.markdown(markdown)
    else:
        st.error("la ruta del documento no existe")