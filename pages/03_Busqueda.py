from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st

import src.utils.web_manager as wb 
import src.utils.helpers as hp
import src.visuals.tablas as tb


st.title("Página de Búsqueda")
wb.opcion_sidebar()

dataset = st.session_state.dataset_actual
if not dataset:
    st.warning("Por favor seleccioná un dataset desde el menú lateral.")
    st.stop()

RUTA_DATASET = Path("processed_datasets") / dataset

archivo = next(RUTA_DATASET.iterdir(), None)
if archivo is None:
    st.error("No hay archivo en la carpeta")
    st.stop()

if dataset == "iadiza":
    df = pd.read_csv(archivo, sep="\t")
else:
    df = pd.read_csv(archivo)


# Función 2.A - Ana Freitas  
with st.expander("Búsqueda por texto Libre", expanded=False):
    df_resultados, archivo_encontrado, columna_seleccionada, termino_busqueda = tb.busqueda_texto_libre()

    if df_resultados is not None:
        st.write(f"Registros encontrados: {len(df_resultados)}")
        st.dataframe(df_resultados, use_container_width=True, key="tabla_libre")
    else:
        df_resultados = None
        termino_busqueda = None


# Filtros para ejercicio 2.b - Fe Cordoba
nombres_cientificos = hp.obtener_opciones(df, "scientificName")
if (dataset != 'xenocanto'):
    provincias = hp.obtener_opciones(df, "stateProvince")
    paises = hp.obtener_paises_validos(df)
else: 
    paises = hp.obtener_opciones(df, "country")

# Función 2.B - Fe Cordoba
with st.expander("Búsqueda de ocurrencias", expanded=False):
    st.markdown("### Selección de ocurrencias específicas")
    filtro_nombre = st.multiselect("Nombre científico", nombres_cientificos)
    filtro_observador = st.text_input("Observador")
    filtro_pais = st.multiselect("País", paises)
    
    if (dataset == 'xenocanto'):
        filtro_provincia = []
    else:
        filtro_provincia = st.multiselect("Provincia", provincias)
        
    if(dataset != "iadiza"):
        fecha_inicio = st.date_input("Fecha inicio")
        fecha_fin = st.date_input("Fecha fin")
    else:
        fecha_fin = None
        fecha_inicio = None

    df_filtrado = wb.aplicar_filtros(
        df,
        nombres_cientificos=filtro_nombre,
        observador=filtro_observador,
        paises=filtro_pais,
        provincias=filtro_provincia,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )

    st.write(f"### Registros encontrados: {len(df_filtrado)}")
    st.dataframe(df_filtrado, use_container_width=True, key="tabla_avanzada")

match dataset:
    case 'iadiza':
        col_id = 'gbifID'
    case 'xenocanto':
        col_id = 'id'
    case 'inaturalist':
        col_id = 'id'

if df_resultados is not None and not df_resultados.empty and termino_busqueda:
    if df_filtrado is not None and not df_filtrado.empty and (filtro_nombre or filtro_observador or filtro_pais or filtro_provincia):
        df_final_busqueda = pd.concat([df_resultados, df_filtrado], ignore_index=True)
    else:
        df_final_busqueda = df_resultados.copy()
    if col_id in df_final_busqueda.columns:
        df_final_busqueda = df_final_busqueda.drop_duplicates(subset=[col_id])
    else:
        df_final_busqueda = df_final_busqueda.drop_duplicates()
else:
    tiene_filtros_avanzados = any([filtro_nombre, filtro_observador, filtro_pais, filtro_provincia])
    if tiene_filtros_avanzados:
        df_final_busqueda = df_filtrado.copy().drop_duplicates()
    else:
        df_final_busqueda = df.copy()


st.markdown("---")
st.subheader("Visualización en Mapa")

if st.button("Ver mapa y ficha técnica del subconjunto", type="primary", use_container_width=True):
    st.session_state["dataset_path"] = str(archivo)
    
    if df_resultados is not None and not df_resultados.empty and termino_busqueda:
        st.session_state["columna_busqueda"] = columna_seleccionada
        st.session_state["texto_busqueda"] = termino_busqueda
    else:
        st.session_state["columna_busqueda"] = None
        st.session_state["texto_busqueda"] = None

    if filtro_nombre or filtro_observador or filtro_pais or filtro_provincia:
        st.session_state["filtro_nombre"] = filtro_nombre
        st.session_state["filtro_observador"] = filtro_observador
        st.session_state["filtro_pais"] = filtro_pais
        st.session_state["filtro_provincia"] = filtro_provincia
        st.session_state["fecha_inicio"] = fecha_inicio
        st.session_state["fecha_fin"] = fecha_fin
    else:
        st.session_state["filtro_nombre"] = []
        st.session_state["filtro_observador"] = ""
        st.session_state["filtro_pais"] = []
        st.session_state["filtro_provincia"] = []
        st.session_state["fecha_inicio"] = None
        st.session_state["fecha_fin"] = None

    st.switch_page("pages/07_Ficha_de_datos.py")

# Función 2.D - Botón de descarga de la tabla en formato CSV - Lúcia Cipolla
para_exportar = wb.exportar_resultados(df_final_busqueda) 
if para_exportar is not None:
    st.download_button(
        label='Exportar Resultados Filtrados (CSV)',
        data=para_exportar,
        file_name=f"{dataset}-{datetime.now().strftime('%d-%m-%y')}.csv",
        mime='text/csv',
        use_container_width=True
    )
st.markdown("---")

# Función 2.C - Agustin Garcia
tb.mostrar_resultados(df_final_busqueda, st.session_state.dataset_actual)

nombre_dataset = st.session_state.get('dataset_actual', 'default')
col_especie = "scientificName"
col_observador = "recordedBy"

if nombre_dataset == 'xenocanto':
    col_pais = "country"
    col_provincia = None  
else:
    col_pais = "countryCode"
    col_provincia = "stateProvince"


# Función 2.E - Sofia Martins
st.subheader("Resumen estadístico del subconjunto mostrado:")
if len(df_final_busqueda) > 0:
    especies = df_final_busqueda[col_especie].nunique() if col_especie in df_final_busqueda.columns else 0
    paises = df_final_busqueda[col_pais].nunique() if (col_pais and col_pais in df_final_busqueda.columns) else 0
    provincias = df_final_busqueda[col_provincia].nunique() if (col_provincia and col_provincia in df_final_busqueda.columns) else 0
    observadores = df_final_busqueda[col_observador].nunique() if col_observador in df_final_busqueda.columns else 0

    st.markdown(f"* **Cantidad de especies únicas:** {especies}")
    st.markdown(f"* **Cantidad de países representados:** {paises}")
    st.markdown(f"* **Cantidad de provincias representadas:** {provincias}")
    st.markdown(f"* **Cantidad de observadores que participaron:** {observadores}")
else:
    st.info("No hay datos para mostrar el resumen estadístico.")
