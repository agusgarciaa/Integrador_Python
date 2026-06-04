from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

import src.utils.web_manager as wb 
import src.visuals.graficos as gr
import src.operaciones.lecturas as lec

st.set_page_config(page_title="Visualización - Gráficos", layout="wide")

wb.opcion_sidebar()

# 2. Título principal de la página P4
st.title("Página de Visualización - Gráficos")

dataset = st.session_state.dataset_actual

if not dataset:
    st.warning("Por favor seleccioná un dataset desde el menú lateral antes de continuar.")
    st.stop()  # Detiene la ejecución del resto de la página

RUTA_DATASET = Path("processed_datasets") / dataset

archivo = next(RUTA_DATASET.iterdir(), None)

if dataset == "iadiza":
    df = pd.read_csv(archivo, sep="\t")
else:
    df = pd.read_csv(archivo)
    

# Llamar al ejercicio 3.A - Ana Freitas
gr.graficar_registros_por_ubicacion()


# Llamar al ejercicio 3.C - Agustin Garcia
gr.grafico_distribucion_taxonomica(df, dataset)


# Llamar al ejercicio 3.D - Fe Cordoba
gr.gr_porcentaje_nulos(dataset,archivo)


st.subheader("cantidad de registros por año")
if "eventDate" in df.columns:
    df_temporal=df.copy()
    df_temporal["eventDate"] = pd.to_datetime(df_temporal["eventDate"],errors='coerce',format='mixed',utc=True).dt.tz_localize(None)
    excluidos=len(df)-df_temporal["eventDate"].notna().sum()
    
    if df_temporal["eventDate"].notna().sum()>0:
        df_definitivo=df_temporal[["eventDate"]].dropna().copy()
        df_definitivo["año"]=df_definitivo["eventDate"].dt.year
        años=df_definitivo.groupby("año").size()
        st.line_chart(años)
        st.write(f"registros excluidos: {excluidos}")
    else:
        st.warning("no hay registros con fechas validas para el grafico")
else:
    st.warning("no existe la columna eventDate en el dataset")


#Ejercicio 3.E - Lucía Cipolla
st.subheader('Tabla comparativa')
datos_raw = wb.tabla_comparativa_datasets()
dataframe_tabla = pd.DataFrame(datos_raw).T
if not dataframe_tabla.empty:
    tabla_formateada = dataframe_tabla.style.format({
        'Registros Totales':'{:.0f}',
        'Coordenadas Validas':'{:.0f}',
        'Fechas Validas':'{:.0f}',
        'Registros Completos':'{:.0f}'
    }).set_properties(**{'text-align':'center'})
    st.table(tabla_formateada)
else:
    st.info('La tabla está vacía')