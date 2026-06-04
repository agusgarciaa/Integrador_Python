import streamlit as st
import pandas as pd

import src.utils.web_manager as wb 
from src.visuals.mapas import mostrar_mapa_interactivo
from src.visuals.mapas import mostrar_ficha_registro
from src.visuals.multimedia import mostrar_multimedia

st.set_page_config(page_title="Ficha de Datos - Mapa", layout="wide")

st.title("Ficha de Datos")
st.markdown("Visualización geográfica de las ocurrencias seleccionadas.")

if "dataset_path" not in st.session_state:
    st.warning(
        "⚠️ No se encontraron parámetros de búsqueda activos. Por favor, realice una consulta en la página de búsqueda primero."
    )
    if st.button("Ir a la Página de Búsqueda"):
        st.switch_page("pages/03_Busqueda.py")
    st.stop()

# Levantamos las variables guardadas
path_archivo = st.session_state.get("dataset_path")
columna = st.session_state.get("columna_busqueda")
texto = st.session_state.get("texto_busqueda")


try:
    separador_caracter = "\t" if "iadiza" in str(path_archivo).lower() else ","
    
    df_original = wb.dataframe_dataset(path_archivo, separador=separador_caracter)
    
    if texto:
        mascara = df_original[columna].astype(str).str.contains(
            texto, 
            case=False, 
            na=False
        )
        df_busqueda1 = df_original[mascara].copy()
    else:
        df_busqueda1 = df_original.copy()

    # Usamos .get() por si algún filtro quedó vacío, para que devuelva None y no rompa la función
    df_busqueda2 = wb.aplicar_filtros(
    	df_original,
    	nombres_cientificos=st.session_state.get("filtro_nombre"),
    	observador=st.session_state.get("filtro_observador"),
    	paises=st.session_state.get("filtro_pais"),
    	provincias=st.session_state.get("filtro_provincia"),
    	fecha_inicio=st.session_state.get("fecha_inicio"),
    	fecha_fin=st.session_state.get("fecha_fin")
	)

    df_busqueda_final = pd.concat(
        [df_busqueda1, df_busqueda2],
        ignore_index=True
    ).drop_duplicates()

    #st.write("Resultados 2.a:", len(df_busqueda1))
    #st.write("Resultados 2.b:", len(df_busqueda2))
    #st.write("Resultado final:", len(df_busqueda_final))

    # Envio el dataset final cruzado al mapa
    if df_busqueda_final.empty:
        st.info("La búsqueda combinada no arrojó resultados para graficar en el mapa.")
    else:

        mostrar_mapa_interactivo(df_busqueda_final)
        mostrar_ficha_registro(df_busqueda_final, st.session_state.dataset_actual)
        match st.session_state.dataset_actual:
            case 'xenocanto':
                st.subheader('Galería de Audio')
            case 'inaturalist':
                st.subheader('Galería de Imágenes')
            case _:
                st.info('El dataset no tiene multimedia')
        mostrar_multimedia(st.session_state.dataset_actual)

except Exception as e:
    st.error(f"Error al reconstruir los datos para el mapa: {e}")