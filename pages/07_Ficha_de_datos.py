# pages/07_Ficha_de_Datos.py
import streamlit as st
from src.mapas import mostrar_mapa_interactivo

st.set_page_config(page_title="Ficha de Datos - Mapa", layout="wide")

st.title("Ficha de Datos")
st.markdown("Visualización geográfica de las ocurrencias seleccionadas.")

# Validamos que existan datos cargados en la sesión
if "resultados_busqueda" not in st.session_state:
    st.warning(
        "⚠️ No se encontraron resultados de búsqueda. Por favor, realice una consulta en la página de búsqueda primero."
    )
    if st.button("Ir a la Página de Búsqueda"):
        st.switch_page("pages/03_Busqueda.py")
    st.stop()

# Llamada de la fúncion y pasamos el DataFrame guardado en la sesión
df_busqueda = st.session_state["resultados_busqueda"]
mostrar_mapa_interactivo(df_busqueda) 