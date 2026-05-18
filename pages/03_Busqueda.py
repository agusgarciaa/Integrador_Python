import streamlit as st
import src.webmanager as wb 
import src.validaciones as va
import pandas as pd
from pathlib import Path

from datetime import datetime


wb.opcion_sidebar()
dataset = st.session_state.dataset_actual

RUTA_DATASET = Path("processed_datasets") / dataset


st.title("Página de Búsqueda (P3)")

# Llamamos a la función del Ejercicio 2.A que acabamos de crear 
df_resultados = wb.mostrar_busqueda_texto_libre()

# Mostrar la tabla interactiva 
if df_resultados is not None:
    st.write(f"Registros encontrados: {len(df_resultados)}")
    st.dataframe(df_resultados)


# 2.b Fe Cordoba
# Cargar dataset
archivo = next(RUTA_DATASET.iterdir(), None)

if archivo is None:
    st.error("No hay archivo en la carpeta")
    st.stop()

if dataset == "iadiza":

    df = pd.read_csv(
        archivo,
        sep="\t"
    )
else:

    df = pd.read_csv(archivo)
    
st.write(df.columns) #en iadiza con y sin tab muestra todo en una columna y anda mal 


# Opciones dinámicas
nombres_cientificos = wb.obtener_opciones(
    df,
    "scientificName"
)

#acomodar para xenocanto
provincias = wb.obtener_opciones(
    df,
    "stateProvince"
)
#acomodar para xenocanto
paises = wb.obtener_paises_validos(df)

# Interfaz
st.title("Búsqueda de ocurrencias")

filtro_nombre = st.multiselect(
    "Nombre científico",
    nombres_cientificos 
)

filtro_observador = st.text_input(
    "Observador"
)

filtro_pais = st.multiselect(
    "País",
    paises
)

filtro_provincia = st.multiselect(
      "Provincia",
       provincias
    )

fecha_inicio = st.date_input(
    "Fecha inicio"
)

fecha_fin = st.date_input(
    "Fecha fin"
)

# Aplicar filtros

df_filtrado = wb.aplicar_filtros(
    df,
    nombres_cientificos=filtro_nombre,
    observador=filtro_observador,
    paises=filtro_pais,
    provincias=filtro_provincia,
    fecha_inicio=fecha_inicio,
    fecha_fin=fecha_fin
)

# Mostrar resultados

st.write(
    f"Resultados encontrados: {len(df_filtrado)}"
)

st.dataframe(df_filtrado)


# Botón de descarga de la tabla en formato CSV
para_exportar = wb.exportar_resultados(df_resultados)
if (para_exportar is not None):
    st.download_button(label='Exportar Resultados',
                    data=para_exportar,
                    file_name=f'{dataset}-{datetime.now().strftime('%d/%m/%y')}.csv',
                    mime='text/csv')