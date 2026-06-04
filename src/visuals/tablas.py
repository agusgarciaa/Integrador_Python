from pathlib import Path

import pandas as pd
import streamlit as st 

import src.operaciones.actualizaciones as act
import src.utils.web_manager as wb 
import src.utils.helpers as hp
import src.utils.constantes as const

# Función 2.A - Ana Freitas
def busqueda_texto_libre():
    """
    Se encarga de la interfaz de búsqueda por texto libre.
    Lee el dataset activo en la sesión y aplica el filtro reutilizando la función registrar_filtro (5.A) de la primera etapa.
    """

    if "dataset_actual" not in st.session_state or st.session_state.dataset_actual is None or st.session_state.dataset_actual == "":
        st.warning("Por favor, seleccione un dataset válido en el menú lateral antes de continuar.")
        return

    nombre_dataset = st.session_state.dataset_actual
    
    separador_caracter = "\t" if nombre_dataset == "iadiza" else ","
    ruta_carpeta = Path("processed_datasets") / nombre_dataset
    archivo_encontrado = None
    
    if ruta_carpeta.exists():
        for elemento_archivo in ruta_carpeta.iterdir():
            if elemento_archivo.is_file():
                archivo_encontrado = elemento_archivo
                break

    if not archivo_encontrado:
        st.error("No se encontró el archivo de datos para este dataset.")
        return

    dataframe_completo = wb.dataframe_dataset(archivo_encontrado, separador=separador_caracter)

    st.subheader("Búsqueda por texto libre")
 
    columnas_disponibles = dataframe_completo.columns.tolist()
    columna_seleccionada = st.selectbox(
        "Seleccione la columna por la que desea buscar:",
        options=columnas_disponibles
    )
    
    termino_busqueda = st.text_input(f"Ingrese el valor que pretende encontrar en '{columna_seleccionada}':").strip()
    
    if not termino_busqueda:
        return dataframe_completo, archivo_encontrado, columna_seleccionada, termino_busqueda

    filas_filtradas_lista = act.registrar_filtro(
        path=str(archivo_encontrado), 
        c_delimiter=separador_caracter, 
        **{columna_seleccionada: termino_busqueda}
    )
    
    if filas_filtradas_lista:
        dataframe_filtrado = pd.DataFrame(filas_filtradas_lista, columns=columnas_disponibles)
        
        mascara_busqueda = dataframe_filtrado[columna_seleccionada].astype(str).str.contains(
            termino_busqueda, 
            case=False,   
            na=False      
        )
        return dataframe_filtrado[mascara_busqueda], archivo_encontrado, columna_seleccionada, termino_busqueda
    else:
        df_vacio = pd.DataFrame(columns=columnas_disponibles)
        return df_vacio, archivo_encontrado, columna_seleccionada, termino_busqueda


#Función 2.C - Agustin Garcia
def mostrar_resultados(df_resultados, nombre_dataset):
    """
    Muestra los resultados de búsqueda con:
    - Cantidad de registros encontrados
    - Columnas relevantes con ordenamiento
    - Paginación
    - Detalle de registro
    """
    st.subheader(f"**Registros encontrados: {len(df_resultados)}**")

    if df_resultados.empty:
        st.info("No se encontraron registros con los criterios seleccionados.")
        return

    # Columnas relevantes
    columnas_presentes = hp.obtener_columnas_relevantes(nombre_dataset, df_resultados.columns.tolist(), const.COLUMNAS_RELEVANTES)
    df_vista = df_resultados[columnas_presentes].copy()
    df_vista["_index_original"] = df_resultados.index

    # Ordenamiento
    col_orden, col_dir = st.columns(2)
    with col_orden:
        columna_orden = st.selectbox("Ordenar por:", columnas_presentes, key="orden_col")
    with col_dir:
        direccion = st.radio("Dirección:", ["Ascendente", "Descendente"], horizontal=True, key="orden_dir")

    df_vista = df_vista.sort_values(by=columna_orden, ascending=direccion == "Ascendente")

    # Paginación
    if "pagina_actual" not in st.session_state:
        st.session_state.pagina_actual = 1

    # Resetear página si cambia el resultado
    if st.session_state.get("_ultimo_hash") != len(df_resultados):
        st.session_state.pagina_actual = 1
        st.session_state._ultimo_hash = len(df_resultados)

    df_pagina, inicio, fin, total_paginas = hp.paginar(df_vista, st.session_state.pagina_actual, const.REGISTROS_POR_PAGINA)

    st.dataframe(df_pagina[columnas_presentes], use_container_width=True, hide_index=True)

    # Controles de paginación
    col_ant, col_info, col_sig = st.columns([1, 2, 1])

    with col_ant:
        if st.button("← Anterior", disabled=st.session_state.pagina_actual == 1, key="btn_ant"):
            st.session_state.pagina_actual -= 1
            st.rerun()

    with col_info:
        st.write(f"Página {st.session_state.pagina_actual} de {total_paginas} — mostrando {inicio + 1} a {fin} de {len(df_resultados)}")

    with col_sig:
        if st.button("Siguiente →", disabled=st.session_state.pagina_actual == total_paginas, key="btn_sig"):
            st.session_state.pagina_actual += 1
            st.rerun()

    # Detalle de registro
    st.markdown("---")

    opciones = {f"Registro #{inicio + i + 1}": idx for i, idx in enumerate(df_pagina["_index_original"])}
    seleccion = st.selectbox("Ver detalle de un registro:", list(opciones.keys()), key="detalle_sel")

    index_original = opciones[seleccion]
    registro = df_resultados.loc[index_original]
    with st.expander(f"Detalle — {seleccion}", expanded=True):
        for campo, valor in registro.items():
            st.write(f"**{campo}:** {valor}")
                