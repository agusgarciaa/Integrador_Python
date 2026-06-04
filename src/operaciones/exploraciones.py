# src/exploraciones.py
from pathlib import Path

import pandas as pd
import streamlit as st

import src.operaciones.validaciones as va
import src.utils.web_manager as wm  
import src.utils.helpers as hp
import src.operaciones.lecturas as lc


def generar_tabla_comparativa():
    ruta_procesados = Path("processed_datasets")

    if not ruta_procesados.exists():
        st.warning("No se encontró la carpeta 'processed_datasets'.")
        return None

    datasets_disponibles = [carpeta.name for carpeta in ruta_procesados.iterdir() if carpeta.is_dir()]

    if not datasets_disponibles:
        st.warning("No se encontraron datasets procesados en el sistema.")
        return None

    datos_comparativos = []

    for dataset in datasets_disponibles:
        separador = "\t" if dataset.lower() == "iadiza" else ","
        ruta_carpeta = ruta_procesados / dataset
        archivo_encontrado = None

        for archivo in ruta_carpeta.iterdir():
            if archivo.is_file():
                archivo_encontrado = archivo
                break

        if archivo_encontrado:
            with st.spinner(f"Analizando {dataset}..."):
                df = wm.dataframe_dataset(archivo_encontrado, separador=separador)
                total_registros = len(df)
                
                if total_registros == 0:
                    continue

                lats_validas = df.apply(va.validar_campo_latitud, axis=1)
                lons_validas = df.apply(va.validar_campo_longitud, axis=1)
                
                coordenadas_ok = (lats_validas == True) & (lons_validas == True)
                porcentaje_coordenadas = (coordenadas_ok.sum() / total_registros) * 100

                col_fecha = 'eventDate' if 'eventDate' in df.columns else ('fecha' if 'fecha' in df.columns else None)
                
                if col_fecha:
                    fechas_validadas = df[col_fecha].apply(va.chequear_fecha)
                    porcentaje_fechas = (fechas_validadas.notnull().sum() / total_registros) * 100
                else:
                    porcentaje_fechas = 0.0

                proporcion_nulos_global = df.isnull().mean().mean()
                promedio_campos_completos = (1 - proporcion_nulos_global) * 100 
                
                datos_comparativos.append({
                    "Dataset": dataset,
                    "Cantidad de registros": total_registros,
                    "Coordenadas válidas (%)": round(porcentaje_coordenadas, 2),
                    "Fechas válidas (%)": round(porcentaje_fechas, 2),
                    "Campos completados prom. (%)": round(promedio_campos_completos, 2)
                })

    if datos_comparativos:
        return pd.DataFrame(datos_comparativos)
    return None


# Funcion 5.B - Fe Cordoba
def dataset_detallado():
    """Muestra un pequeño resumen de 3 aspectos sobre el dataset seleccionado."""

    st.header("Datasets en detalle")

    datasets = hp.obtener_nombres_datasets()

    if datasets:
        dataset_elegido = st.selectbox("Seleccione un dataset para ver en detalle:", datasets)

        if dataset_elegido:
            ruta = Path("processed_datasets") / dataset_elegido
            separador = "\t" if dataset_elegido == "iadiza" else "," 

            archivo_dataset = None
         
            if ruta.exists():
                for archivo in ruta.iterdir():
                    if archivo.is_file():
                        archivo_dataset = archivo

            if archivo_dataset:
                df = pd.read_csv(archivo_dataset, sep=separador)
                lista_columnas = df.columns.to_list()
            
                total_registros = lc.total_registros(archivo_dataset, separador)
            
                diccionario_nulos = lc.porcentaje_nulos(archivo_dataset, separador) 

                st.subheader(f"Ficha técnica del dataset: {dataset_elegido.capitalize()}")
                st.write("Total de registros:", total_registros)
            
                st.write("Ver lista completa de columnas:")
                st.write(lista_columnas)
                
                st.write("Porcentaje de valores nulos por columna")
                df_nulos = pd.DataFrame(list(diccionario_nulos.items()), columns=["Columna", "% de Nulos"])
                st.dataframe(df_nulos)
            else:
                st.error(f"No se encontró ningún archivo dentro de la carpeta {dataset_elegido}")
    else:
        st.error("No hay datasets disponibles")