import streamlit as st 
import src.webmanager as wb 

wb.opcion_sidebar()
dataset = st.session_state.dataset_actual

# Configuración de la página (P1)
st.set_page_config(page_title="BioData Explorer - Inicio", page_icon="🌿", layout="wide")

# --- TÍTULO DE LA APLICACIÓN ---
st.title(" BioData Explorer: Gestión de Biodiversidad")

# --- PROPÓSITO E IMPORTANCIA ---
st.header("Propósito de la aplicación")
st.write(""" Esta aplicación ha sido diseñada como una herramienta interactiva para la gestión y el análisis 
de datos biológicos. Su objetivo es centralizar la información recolectada en campo para facilitar 
la toma de decisiones informadas sobre la conservación de especies.""")

st.header("Importancia del análisis de datos de biodiversidad")
st.write("""El análisis de datos es fundamental para comprender la salud de los ecosistemas. Permite identificar 
patrones de distribución, detectar especies en peligro y evaluar el impacto de los cambios ambientales 
en la biodiversidad global.""")

# --- ESTÁNDAR DARWIN CORE ---
st.header("Estándar Darwin Core (DwC)")
st.info("""El estándar **Darwin Core (DwC)** es un conjunto de términos y definiciones diseñado para 
facilitar el intercambio de información sobre biodiversidad. 

* **¿Qué es?**: Un vocabulario compartido de términos técnicos.
* **¿Para qué se utiliza?**: Se utiliza para estandarizar registros biológicos (observaciones, muestras). 
Permite que datos de distintas instituciones puedan integrarse y compararse sin ambigüedades. """)

# --- INSTRUCCIONES DE USO ---
st.header("Instrucciones básicas de uso")
st.markdown("""P ara explorar la aplicación, utilice el **menú lateral**:
1.  **Inicio**: Información general y contexto del proyecto.
2.  **Estado del sistema**: Resumen estadístico de los datos cargados.
3.  **Búsqueda**:
4.  **Visualización**: """)