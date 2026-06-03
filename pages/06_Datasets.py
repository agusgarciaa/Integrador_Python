# pages/06_Datasets.py
import os
from datetime import datetime
import src.utils.file_manager as fm
import streamlit as st
import src.operaciones.exploraciones as exp
import pandas as pd 
from pathlib import Path
from src.operaciones import lecturas as lc
from src.utils import helpers as hp

st.set_page_config(page_title="Exploración - Datasets", layout="wide")

st.title("Exploración de Datasets")
st.markdown("Vista general y comparativa de todos los datasets disponibles en el sistema.")


# Ejercicio 5.A - Agustin Garcia
DATASETS = {
    "iadiza": "occurrence.txt",
    "inaturalist": "observations.csv",
    "xenocanto": "Occurrence.txt",
}

st.markdown("### Datasets disponibles")

filas = []
for dataset, archivo in DATASETS.items():
    ruta = Path("processed_datasets") / dataset / archivo

    if not ruta.exists():
        ruta = Path("raw_datasets") / dataset / archivo

    if not ruta.exists():
        filas.append({
            "Nombre": dataset.capitalize(),
            "Archivo": archivo,
            "Tamaño": "No disponible",
            "Última modificación": "No disponible",
        })
        continue

    tamaño_mb = f"{round(ruta.stat().st_size / (1024 * 1024), 2)} MB"
    fecha_mod = datetime.fromtimestamp(ruta.stat().st_mtime).strftime("%d/%m/%Y %H:%M:%S")

    filas.append({
        "Nombre": dataset.capitalize(),
        "Archivo": archivo,
        "Tamaño": tamaño_mb,
        "Última modificación": fecha_mod,
    })

df_tabla = pd.DataFrame(filas)
st.dataframe(df_tabla, use_container_width=True, hide_index=True)


# Llamo a Funcion 5.B - Fe Cordoba
exp.dataset_detallado()


st.header("Tabla comparativa de todos los datasets.")

df_comparativo = exp.generar_tabla_comparativa()
if df_comparativo is not None:
    st.dataframe(df_comparativo, use_container_width=True)
   
ruta = fm.obtener_raiz_proyecto() 
ruta_dataset1=ruta / "documentation" / "dataset_a1.md"
ruta_dataset2=ruta / "documentation" / "dataset_a2.md"
ruta_dataset3=ruta / "documentation" / "dataset_a3.md"

documento=st.selectbox("Seleccione el documento markdown que quiere visualizar",["Iadiza","Xeno-canto","iNaturalist"])
if documento:
    if documento=="Iadiza":
        ruta=ruta_dataset1
    elif documento=="Xeno-canto":
        ruta=ruta_dataset2
    elif documento=="iNaturalist":
        ruta=ruta_dataset3
    if os.path.exists(ruta):
        with open(ruta,encoding="utf-8") as archivo:
            markdown=archivo.read()
            st.markdown(markdown)
    else:
        st.error("la ruta del documento no existe")

