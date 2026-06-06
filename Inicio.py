import streamlit as st 

st.set_page_config(page_title="BioData Explorer - Inicio", page_icon="🌿", layout="wide")

pag_inicio = st.Page("pages/01_Home.py", title="Inicio", icon="🌿", default=True)
pag_estado = st.Page("pages/02_Estado_del_sistema.py", title="Estado del Sistema", icon="🖥️")
pag_busqueda = st.Page("pages/03_Busqueda.py", title="Búsqueda", icon="🔎")
pag_visualizacion = st.Page("pages/04_Visualizacion.py", title="Visualización", icon="📊")
pag_gestion = st.Page("pages/05_Gestion_de_registros.py", title="Gestión de Registros", icon="📂")
pag_datasets = st.Page("pages/06_Datasets.py", title="Datasets", icon="💾")

pag_ficha = st.Page("pages/07_Ficha_de_datos.py", title="Ficha de Datos", icon="🗺️")

pg = st.navigation({
    "Principal": [pag_inicio, pag_estado],
    "Herramientas": [pag_busqueda, pag_visualizacion, pag_gestion, pag_datasets, pag_ficha],
})

st.html(
    """
    <style>
        a[href*="Ficha_de_datos"] {
            display: none !important;
        }
    </style>
    """
)

pg.run()