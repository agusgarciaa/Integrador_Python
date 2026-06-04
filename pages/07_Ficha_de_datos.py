import streamlit as st

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

# Levantamos las 3 variables guardadas
path_archivo = st.session_state["dataset_path"]
columna = st.session_state["columna_busqueda"]
texto = st.session_state["texto_busqueda"]

try:
    separador_caracter = "\t" if "iadiza" in path_archivo.lower() else ","
    
    df_original = wb.dataframe_dataset(path_archivo, separador=separador_caracter)
    
    if texto:
        mascara = df_original[columna].astype(str).str.contains(
            texto, 
            case=False, 
            na=False
        )
        df_busqueda = df_original[mascara].copy()
    else:
        df_busqueda = df_original.copy()

    mostrar_mapa_interactivo(df_busqueda)
    mostrar_ficha_registro(df_busqueda, st.session_state.dataset_actual)
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
