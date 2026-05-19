import src.webmanager as wb 
import pandas as pd
import streamlit as st
import src.utils as ut
from pathlib import Path
import matplotlib.pyplot as plt

wb.opcion_sidebar()
dataset = st.session_state.dataset_actual

RUTA_DATASET = Path("processed_datasets") / dataset

archivo = next(RUTA_DATASET.iterdir(), None)

if dataset == "iadiza":
    df = pd.read_csv(archivo, sep="\t")
else:
    df = pd.read_csv(archivo)

st.title("Gráficos")

diccionario_nulos = ut.porcentaje_nulos(archivo)

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

