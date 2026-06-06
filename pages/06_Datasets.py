from datetime import datetime
from pathlib import Path

import os
import streamlit as st
import pandas as pd 

import src.utils.file_manager as fm
import src.operaciones.exploraciones as exp
import src.utils.constantes as const

st.title("Exploración de Datasets")
st.markdown("Vista general, analítica y comparativa de todos los datasets disponibles en el sistema.")
st.markdown("---")

# Ejercicio 5.A - Agustin Garcia
st.header("Archivos físicos del sistema")

filas = []
for dataset, archivo in const.DATASETS.items():
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
st.markdown("---")

tab_analisis, tab_documentacion = st.tabs([
    "Análisis Estadístico y Comparativo", 
    "Documentación Técnica"
])


with tab_analisis:
    st.header("Tabla comparativa de todos los datasets.")
    # Llamo a Funcion 5.C - Ana
    df_comparativo = exp.generar_tabla_comparativa()
    if df_comparativo is not None:
        st.dataframe(df_comparativo, use_container_width=True)
    
    # Llamo a Funcion 5.B - Fe Cordoba 
    exp.dataset_detallado()
    
st.markdown("---")


with tab_documentacion:
    st.header("Visualizador de especificaciones de datos")
    st.write("Seleccione el documento markdown que quiere visualizar",["Iadiza","Xeno-canto","iNaturalist"])
    
    ruta_base = fm.obtener_raiz_proyecto() 
    ruta_dataset1 = ruta_base / "documentation" / "dataset_a1.md"
    ruta_dataset2 = ruta_base / "documentation" / "dataset_a2.md"
    ruta_dataset3 = ruta_base / "documentation" / "dataset_a3.md"

    documento = st.selectbox(
        "Seleccione el documento markdown que quiere visualizar",
        ["Iadiza", "Xeno-canto", "iNaturalist"],
        key="sb_selector_markdown_exploracion"
    )
    
    if documento:
        if documento == "Iadiza":
            ruta_archivo = ruta_dataset1
        elif documento == "Xeno-canto":
            ruta_archivo = ruta_dataset2
        elif documento == "iNaturalist":
            ruta_archivo = ruta_dataset3
            
        st.markdown("---")
        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, encoding="utf-8") as archivo_md:
                markdown_contenido = archivo_md.read()
                with st.container(border=True):
                    st.markdown(markdown_contenido)
        else:
            st.error(f"La ruta del documento para '{documento}' no existe en la carpeta documentation.")

