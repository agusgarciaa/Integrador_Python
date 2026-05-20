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
    df = pd.read_csv(archivo, sep="\t")
else:
    df = pd.read_csv(archivo)
    
# st.write(df.columns) # en iadiza con y sin tab muestra todo en una columna y anda mal 

# Opciones sacadas del dataframe
nombres_cientificos = wb.obtener_opciones(df, "scientificName")

if (dataset != 'xenocanto'):
    provincias = wb.obtener_opciones(df, "stateProvince")
    paises = wb.obtener_paises_validos(df)
else: 
    paises = wb.obtener_opciones(df, "country")

# Interfaz
st.title("Búsqueda de ocurrencias")

filtro_nombre = st.multiselect("Nombre científico", nombres_cientificos )

filtro_observador = st.text_input("Observador")

filtro_pais = st.multiselect("País", paises)

if (dataset == 'xenocanto'):
    filtro_provincia = []
else:
    filtro_provincia = st.multiselect("Provincia", provincias)

fecha_inicio = st.date_input("Fecha inicio")

fecha_fin = st.date_input("Fecha fin")

#st.write(df['recordedBy']) # era para ver q valores tenia esa columna y probar que ande

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
st.write(f"Resultados encontrados: {len(df_filtrado)}")
st.dataframe(df_filtrado)


# Botón de descarga de la tabla en formato CSV
para_exportar = wb.exportar_resultados(df_resultados)
if (para_exportar is not None):
    st.download_button(label='Exportar Resultados',
                    data=para_exportar,
                    file_name=f'{dataset}-{datetime.now().strftime('%d/%m/%y')}.csv',
                    mime='text/csv')
    
nombre_dataset = st.session_state.get('dataset_actual', 'default')

col_especie = "scientificName"
col_observador = "recordedBy"

if nombre_dataset == 'xenocanto':
    col_pais = "country"
    col_provincia = None  
else:
    col_pais = "countryCode"
    col_provincia = "stateProvince"
    
st.subheader("resumen estadistico del subconjunto mostrado:")
if len(df_filtrado)>0:
    especies = df_filtrado[col_especie].nunique() if col_especie in df_filtrado.columns else 0
    paises = df_filtrado[col_pais].nunique() if (col_pais and col_pais in df_filtrado.columns) else 0
    provincias = df_filtrado[col_provincia].nunique() if (col_provincia and col_provincia in df_filtrado.columns) else 0
    observadores = df_filtrado[col_observador].nunique() if col_observador in df_filtrado.columns else 0

    st.markdown(f"cantidad de especies unicas: {especies}")
    st.markdown(f"cantidad de paises representados: {paises}")
    st.markdown(f"cantidad de provincias representadas: {provincias}")
    st.markdown(f"cantidad de observadores que participaron: {observadores}")
else:
    st.markdown("No hay datos para mostrar el resumen estadístico.")