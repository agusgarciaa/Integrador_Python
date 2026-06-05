from pathlib import Path

import pandas as pd
import streamlit as st 
import csv

import src.operaciones.actualizaciones as act
import src.utils.web_manager as wb 
import src.utils.helpers as hp
import src.utils.constantes as const
import src.operaciones.lecturas as lec
import src.utils.file_manager as fm
import src.operaciones.validaciones as va

# Función 2.A - Ana Freitas
def busqueda_texto_libre():
    """
    Se encarga de la interfaz de búsqueda por texto libre usando Pandas 
    para garantizar compatibilidad absoluta con todos los datasets.
    """
    if "dataset_actual" not in st.session_state or st.session_state.dataset_actual is None or st.session_state.dataset_actual == "":
        st.warning("Por favor, seleccione un dataset válido en el menú lateral antes de continuar.")
        return None, None, None, None

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
        return None, None, None, None

    dataframe_completo = wb.dataframe_dataset(archivo_encontrado, separador=separador_caracter)

    st.subheader("Búsqueda por texto libre")
 
    columnas_disponibles = dataframe_completo.columns.tolist()
    columna_seleccionada = st.selectbox(
        "Seleccione la columna por la que desea buscar:",
        options=columnas_disponibles,
        key="sb_columna_libre"
    )
    
    termino_busqueda = st.text_input(f"Ingrese el valor que pretende encontrar en '{columna_seleccionada}':", key="ti_termino_libre").strip()
    
    if not termino_busqueda:
        return dataframe_completo, archivo_encontrado, columna_seleccionada, termino_busqueda

    mascara_busqueda = dataframe_completo[columna_seleccionada].astype(str).str.contains(
        termino_busqueda, 
        case=False,   # Ignora mayúsculas/minúsculas de forma nativa
        na=False      # Ignora los campos nulos sin romper el programa
    )
    
    dataframe_filtrado = dataframe_completo[mascara_busqueda]
    
    return dataframe_filtrado, archivo_encontrado, columna_seleccionada, termino_busqueda

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


#Función 3.E - Lucía Cipolla
def tabla_comparativa_datasets():
    """
        Si hay 2 o más datasets toma todos los datos y retorna lo necesario para armar la tabla comparativa.
        Si hay menos de 2 datasets en "processed_datasets" muestra una advertencia y retorna vacío.
        Si en el proceso de análisis no encuentra los archivos muestra una advertencia y retorna vacío.
    """
    datasets = hp.obtener_nombres_datasets()
    if len(datasets)<2:
        st.warning('Se necesitan al menos dos datasets para comparar')
        return
    
    registros_por_dataset = {}
    for nombre_dataset in datasets:
        datos = 'occurrence.txt' if (nombre_dataset=='iadiza') else 'observations.csv' if (nombre_dataset=='inaturalist') else 'Occurrence.txt'
        ruta_dat = Path("processed_datasets") / nombre_dataset / datos
        if (ruta_dat.is_file()):
            if (nombre_dataset == 'iadiza'):
                registros_por_dataset[nombre_dataset] = lec.total_registros(ruta_dat,'\t')
            else:
                registros_por_dataset[nombre_dataset] = lec.total_registros(ruta_dat)
        else:
            st.error(f'No se encontró el archivo {datos}')
            return
    
    cant_registros_coordenadas_validas = {}
    for nombre_dataset in datasets:
        datos = 'occurrence.txt' if (nombre_dataset=='iadiza') else 'observations.csv' if (nombre_dataset=='inaturalist') else 'Occurrence.txt'
        separador = '\t' if (nombre_dataset=='iadiza') else ','
        ruta = fm.obtener_raiz_proyecto() / 'processed_datasets' / nombre_dataset / datos
        if (ruta.is_file()):
            with open(ruta,encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo ,delimiter=separador)
                cant_registros_coordenadas_validas[nombre_dataset] = 0
                for fila in lector:
                    if (va.es_coordenada_valida(fila)):
                        cant_registros_coordenadas_validas[nombre_dataset] += 1
        else:
            st.error(f'No se encontró el archivo {datos}')
            return
    
    cant_registros_fecha_valida = {}
    for nombre_dataset in datasets:
        datos = 'occurrence.txt' if (nombre_dataset=='iadiza') else 'observations.csv' if (nombre_dataset=='inaturalist') else 'Occurrence.txt'
        separador = '\t' if (nombre_dataset=='iadiza') else ','
        ruta = fm.obtener_raiz_proyecto() / 'processed_datasets' / nombre_dataset / datos
        if (ruta.is_file()):
            with open(ruta,encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo ,delimiter=separador)
                if ('eventDate' not in lector.fieldnames) and ('verbatimEventDate' not in lector.fieldnames):
                    st.warning(f'No hay columnas de fecha en {nombre_dataset}')
                    continue
                
                cant_registros_fecha_valida[nombre_dataset] = 0
                for fila in lector:
                    if (va.chequear_fecha(fila.get('eventDate')) is not None) or (va.chequear_fecha(fila.get('verbatimEventDate')) is not None):
                        cant_registros_fecha_valida[nombre_dataset] += 1
        else:
            st.error(f'No se encontró el archivo {datos}')
            return
        
    cant_campos_completos_promedio = {}
    for nombre_dataset in datasets:
        datos = 'occurrence.txt' if (nombre_dataset=='iadiza') else 'observations.csv' if (nombre_dataset=='inaturalist') else 'Occurrence.txt'
        separador = '\t' if (nombre_dataset=='iadiza') else ','
        ruta = fm.obtener_raiz_proyecto() / 'processed_datasets' / nombre_dataset / datos
        if (ruta.is_file()):
            lector = pd.read_csv(ruta,delimiter=separador,encoding='utf-8')
            lector = lector.replace(r'^\s*$', None, regex=True)
            porcentaje_completadas = lector.notna().mean().mean() * 100
            
            if (porcentaje_completadas > 0):
              cant_campos_completos_promedio[nombre_dataset] = porcentaje_completadas
            else:
                cant_campos_completos_promedio[nombre_dataset] = 0
        else:
            st.error(f'No se encontró el archivo {datos}')
            return
    
    ret = {}
    for nombre in datasets:
        ret[nombre] = {'Registros Totales': registros_por_dataset.get(nombre,0),
                       'Coordenadas Validas': cant_registros_coordenadas_validas.get(nombre,0),
                       'Fechas Validas': cant_registros_fecha_valida.get(nombre,0),
                       'Registros Completos': cant_campos_completos_promedio.get(nombre,0)}
    return ret  