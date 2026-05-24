# src/exploraciones.py
from pathlib import Path

import pandas as pd
import streamlit as st

import src.validaciones as va
import src.web_manager as wm  


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