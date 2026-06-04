import streamlit as st
import pandas as pd
import os
import csv


def filtrar_logs(ruta):

    """Muestra la interfaz de filtrado y métricas para el archivo de logs."""

    df_logs = pd.read_csv(ruta, sep="|", names=["fecha", "dataset", "operacion", "registros", "estado"])
    df_logs['operacion'] = df_logs['operacion'].str.strip()

    # Columna de fecha a tipo datetime para poder comparar
    df_logs['fecha'] = pd.to_datetime(df_logs['fecha'])

    # Widgets de filtrado
    st.subheader("Filtros de búsqueda")

    opciones = ["INSERT", "UPDATE", "DELETE", "VALIDATION"]
    operaciones_seleccionadas = st.multiselect("Filtrar por operación:", options=opciones)

    # Pedimos las fechas por separado usando columnas para que queden lado a lado
    col_inicio, col_fin = st.columns(2)

    with col_inicio:
     # Widget para fecha de inicio
        input_inicio = st.date_input("Seleccione la fecha de inicio:")

    with col_fin:
     # Widget para fecha de fin
        input_fin = st.date_input("Seleccione la fecha de fin:")

    # Filtros 
    df_filtrado = df_logs.copy() 

    if len(operaciones_seleccionadas) > 0:
      df_filtrado = df_filtrado[df_filtrado['operacion'].isin(operaciones_seleccionadas)]

    df_filtrado = df_filtrado[(df_filtrado['fecha'].dt.date >= input_inicio) & (df_filtrado['fecha'].dt.date <= input_fin)]

    # Métricas resumidas
    st.write("### Métricas resumidas del log filtrado")

    total_insert = len(df_filtrado[df_filtrado['operacion'] == 'INSERT'])
    total_update = len(df_filtrado[df_filtrado['operacion'] == 'UPDATE'])
    total_delete = len(df_filtrado[df_filtrado['operacion'] == 'DELETE'])
    total_validation = len(df_filtrado[df_filtrado['operacion'] == 'VALIDATION'])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.write(f"**Inserciones:** {total_insert}")
    with c2:
        st.write(f"**Actualizaciones:** {total_update}")
    with c3:
        st.write(f"**Eliminaciones:** {total_delete}")
    with c4:
        st.write(f"**Validaciones:** {total_validation}")

    # Mostrar la tabla interactiva
    st.write("### Logs filtrados")
    st.dataframe(df_filtrado)


# 8.c Mostrar logs tabulados y sus metricas
def logs_tabulados(ruta):
    """Muestra todos los logs tabulados y sus métricas."""

    st.header('Logs totales')
    st.subheader("Métricas resumidas de todos los logs")

    df_logs = pd.read_csv(ruta, sep="|", names=["fecha", "dataset", "operacion", "registros", "estado"])
    df_logs["operacion"] = df_logs["operacion"].str.strip()

    c1_g, c2_g, c3_g, c4_g = st.columns(4)
    with c1_g:
        st.write(f"**Inserciones:** {len(df_logs[df_logs['operacion'] == 'INSERT'])}")
    with c2_g:
        st.write(f"**Actualizaciones:** {len(df_logs[df_logs['operacion'] == 'UPDATE'])}")
    with c3_g:
        st.write(f"**Eliminaciones:** {len(df_logs[df_logs['operacion'] == 'DELETE'])}")
    with c4_g:
        st.write(f"**Validaciones:** {len(df_logs[df_logs['operacion'] == 'VALIDATION'])}")

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