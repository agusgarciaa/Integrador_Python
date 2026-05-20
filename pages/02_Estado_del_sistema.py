from pathlib import Path
import os
import csv
import streamlit as st 
import src.utils as ut
import src.webmanager as wb 

st.title("Logs generados.")

ruta = ut.obtener_ruta_log("logs", "operations.log")

if os.path.exists(ruta):
    datos_tabla = []
    encabezados = ["Fecha", "Dataset", "Operación", "Registros", "Estado"]
    datos_tabla.append(encabezados)

    try:
        with open(ruta, "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter="|")
            for fila in reader:
                fila_limpia = [campo.strip() for campo in fila]
                if fila_limpia:
                    datos_tabla.append(fila_limpia)
        
        if len(datos_tabla) > 1:
            st.table(datos_tabla)
        else:
            st.info("El archivo de log está vacío.")
            
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
else:
    st.error(f"El archivo {ruta} no existe.")