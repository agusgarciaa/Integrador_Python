from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

import src.web_manager as wb 
import src.graficos as gr
import src.lecturas as lec

st.set_page_config(page_title="Visualización - Gráficos", layout="wide")

wb.opcion_sidebar()

# 2. Título principal de la página P4
st.title("Página de Visualización")

# Llamar al ejercicio 3.A - Ana Freitas
gr.graficar_registros_por_ubicacion()

st.title("Gráficos")
dataset = st.session_state.dataset_actual
RUTA_DATASET = Path("processed_datasets") / dataset

archivo = next(RUTA_DATASET.iterdir(), None)

if dataset == "iadiza":
    df = pd.read_csv(archivo, sep="\t")
else:
    df = pd.read_csv(archivo)

#3.D Fe Cordoba
"""Calcula y grafica el porcentaje de datos no nulos por columna."""
diccionario_nulos = lec.porcentaje_nulos(archivo)

# Creamos una Serie de Pandas con ese diccionario
serie_nulos = pd.Series(diccionario_nulos)

# Restamos a cada valor
serie_no_nulos = 100.0 - serie_nulos

# Ordenamos de menor a mayor por que el grafico se construye de abajo hacia arriba
serie_ordenada = serie_no_nulos.sort_values(ascending=True)

# Creamos gráfico
ax = serie_ordenada.plot(
    kind='barh',
    figsize=(12, 18)
)

# Título
ax.set_title("Porcentaje de valores no nulos por columna")

# Etiquetas de ejes
ax.set_xlabel("Porcentaje")
ax.set_ylabel("Columnas")

# Tamaño de texto del eje Y
ax.tick_params(axis='y', labelsize=11)

# Ajuste automático
plt.tight_layout()

# Obtener figura
fig = ax.get_figure()

st.pyplot(fig)

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
