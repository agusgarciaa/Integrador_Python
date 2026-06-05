from pathlib import Path

import pandas as pd
import streamlit as st

import src.utils.web_manager as wb 
import src.visuals.graficos as gr
import src.visuals.tablas as tb


st.title("Página de Visualización")
wb.opcion_sidebar()

dataset = st.session_state.dataset_actual

if not dataset:
    st.warning("Por favor seleccioná un dataset desde el menú lateral antes de continuar.")
    st.stop() 

RUTA_DATASET = Path("processed_datasets") / dataset
archivo = next(RUTA_DATASET.iterdir(), None)

if dataset == "iadiza":
    df = pd.read_csv(archivo, sep="\t")
else:
    df = pd.read_csv(archivo)


tab_ubicacion, tab_taxonomica, tab_nulos, tab_temporal, tab_comparativa = st.tabs([
    "registros por ubicación",
    "distribución taxonomica",
    "porcentaje nulos",
    "registros por año",
    "tabla comparativa"
])

with tab_ubicacion:
    # Llamar al ejercicio 3.A - Ana Freitas
    st.subheader("Grafico distribución geográfica de registros")
    gr.graficar_registros_por_ubicacion(df)


with tab_taxonomica:
    # Llamar al ejercicio 3.C - Agustin Garcia
    st.subheader("Grafico distribucion taxonomica")
    gr.graficar_distribucion_taxonomica(df, dataset)


with tab_nulos:
    # Llamar al ejercicio 3.D - Fe Cordoba
    st.subheader("Grafico sobre el porcentaje de datos no nulos por columna")
    gr.graficar_porcentaje_nulos(dataset, archivo)


# Función 3.B - Sofia Martins
with tab_temporal:
    st.subheader("Grafico cantidad de registros por año")
    if "eventDate" in df.columns:
        df_temporal = df.copy()
        df_temporal["eventDate"] = pd.to_datetime(df_temporal["eventDate"], errors='coerce', format='mixed', utc=True).dt.tz_localize(None)
        excluidos = len(df) - df_temporal["eventDate"].notna().sum()
        
        if df_temporal["eventDate"].notna().sum() > 0:
            df_definitivo = df_temporal[["eventDate"]].dropna().copy()
            df_definitivo["año"] = df_definitivo["eventDate"].dt.year
            años = df_definitivo.groupby("año").size()
            
            st.line_chart(años)
            st.write(f"registros excluidos: {excluidos}")
        else:
            st.warning("no hay registros con fechas validas para el grafico")
    else:
        st.warning("no existe la columna eventDate en el dataset")

with tab_comparativa:
    # Ejercicio 3.E - Lucía Cipolla)
    st.subheader('Tabla comparativa')
    datos_raw = tb.tabla_comparativa_datasets()
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
