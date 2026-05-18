import streamlit as st
import src.webmanager as wb 



wb.opcion_sidebar()
dataset = st.session_state.dataset_actual


# 2. Título de la página de búsqueda (P3)
st.title("Página de Búsqueda (P3)")

# 3. Llamamos a la función del Ejercicio 2.A que acabamos de crear
# Esta función dibuja los inputs y filtra los datos de Pandas
df_resultados = wb.mostrar_busqueda_texto_libre()

# --- Avance del Ejercicio 2.C (Mostrar la tabla interactiva) ---
if df_resultados is not None:
    st.write(f"Registros encontrados: {len(df_resultados)}")
    st.dataframe(df_resultados) # Muestra la tabla interactiva [cite: 52]