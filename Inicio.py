import streamlit as st 
import src.utils.web_manager as wb 

# Configuración de la página (P1)
st.set_page_config(page_title="BioData Explorer - Inicio", page_icon="🌿", layout="wide")

wb.opcion_sidebar()
dataset = st.session_state.dataset_actual

# --- TÍTULO DE LA APLICACIÓN ---
st.title("BioData Explorer: Gestión de Biodiversidad")

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
st.markdown("""
Para explorar la aplicación, utilice el **menú lateral**:

1. **Inicio (P1)**: Información general, integrantes y contexto del proyecto.
2. **Estado del sistema (P2)**: Resumen estadístico, calidad y estado de los datos cargados.
3. **Búsqueda (P3)**: Permite localizar registros específicos dentro del dataset aplicando múltiples filtros combinables y visualizar tablas de resultados.
4. **Visualización (P4)**: Presentación gráfica de la biodiversidad mediante gráficos estadísticos interactivos y mapas de distribución general.
5. **Gestión de registros (P5)**: Panel interactivo para insertar, actualizar y eliminar registros del sistema de forma segura, con auditoría en el log de operaciones.
6. **Exploración de datasets (P6)**: Vista global e independiente para comparar y explorar todos los archivos de datos disponibles en el sistema.

*Nota: Al seleccionar un registro específico en la página de **Búsqueda (P3)** y presionar el botón de acción, el sistema lo redirigirá automáticamente a la **Ficha de datos (P7)** para analizar su mapa de ocurrencia detallado y sus archivos multimedia asociados.*
""")