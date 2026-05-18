import streamlit as st
import src.webmanager as wb 

from datetime import datetime

wb.opcion_sidebar()
dataset = st.session_state.dataset_actual

st.title("Página de Búsqueda (P3)")

# Llamamos a la función del Ejercicio 2.A que acabamos de crear 
df_resultados = wb.mostrar_busqueda_texto_libre()

# Mostrar la tabla interactiva 
if df_resultados is not None:
    st.write(f"Registros encontrados: {len(df_resultados)}")
    st.dataframe(df_resultados)

# Botón de descarga de la tabla en formato CSV
para_exportar = wb.exportar_resultados(df_resultados)
if (para_exportar is not None):
    st.download_button(label='Exportar Resultados',
                    data=para_exportar,
                    file_name=f'{dataset}-{datetime.now().strftime('%d/%m/%y')}.csv',
                    mime='text/csv')