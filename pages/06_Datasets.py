# pages/06_Datasets.py
import os
import src.file_manager as fm
import streamlit as st
from src.exploraciones import generar_tabla_comparativa
import pandas as pd 
from pathlib import Path
from src import lecturas as lc
from src import helpers as hp

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

documento=st.selectbox("Seleccione el documento markdown que quiere visualizar",["dataset1","dataset2","dataset3"])
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


# 5.b Fe Cordoba
st.header("Datasets en detalle")

datasets = hp.obtener_nombres_datasets()

if datasets:
    dataset_elegido = st.selectbox("Seleccione un dataset para ver en detalle:", datasets)

    if dataset_elegido:
        ruta = Path("processed_datasets") / dataset_elegido
        separador = "\t" if dataset_elegido == "iadiza" else "," 

        archivo_dataset = None
        
        # Buscamos el archivo dentro de la carpeta iterando 
        if ruta.exists():
            for archivo in ruta.iterdir():
                if archivo.is_file():
                    archivo_dataset = archivo

        if archivo_dataset:
            # me quedo con las columnas
            df = pd.read_csv(archivo_dataset, sep=separador)
            lista_columnas = df.columns.to_list()
            
            # me quedo con el total de regs
            total_registros = lc.total_registros(archivo_dataset, separador)
            
            # me quedo con los % de nulos por cols
            diccionario_nulos = lc.porcentaje_nulos(archivo_dataset, separador) 

            # Mostrar la información
            st.subheader(f"Ficha técnica del dataset: {dataset_elegido.capitalize()}")
            st.write("Total de registros:", total_registros)
            
            st.write("Ver lista completa de columnas:")
            st.write(lista_columnas)
                
            st.write("Porcentaje de valores nulos por columna")
            # Convertimos el diccionario a DataFrame para que quede como una tabla linda
            df_nulos = pd.DataFrame(list(diccionario_nulos.items()), columns=["Columna", "% de Nulos"])
            st.dataframe(df_nulos)
        else:
            st.error(f"No se encontró ningún archivo dentro de la carpeta {dataset_elegido}")
else:
    st.error("No hay datasets disponibles")
