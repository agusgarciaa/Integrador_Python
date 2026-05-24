from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt

import src.helpers as hp
import src.validaciones as va
import src.lecturas as lec
import src.actualizaciones as act


#funcion 1.a sofia martins
def dataframe_dataset(nombre,separador=','):
    dataframe=pd.read_csv(nombre,sep=separador,encoding='utf-8')
    return dataframe

#Funcion 1.b y C - Fe Cordoba, Agustin Garcia
def opcion_sidebar(separador=','):
    """
    Configura la barra lateral de Streamlit para la selección del dataset.
    """
    datasets = hp.obtener_nombres_datasets()
    if not datasets:
        st.sidebar.error("No hay datasets disponibles")
        return

    if "dataset_actual" not in st.session_state:
        st.session_state.dataset_actual = None

    if "fecha_seleccion" not in st.session_state:
        st.session_state.fecha_seleccion = None

    dataset_actual = st.session_state.dataset_actual

    opciones = ["Seleccionar dataset:"] + datasets

    indice_dataset = 0  # Muestra por defecto seleccionar dataset: como placeholder

    if dataset_actual in datasets:
        indice_dataset = datasets.index(dataset_actual) + 1  # +1 por el placeholder

    dataset_seleccionado = st.sidebar.selectbox(
        "Seleccione un dataset:",
        opciones,
        index=indice_dataset
    )

    if dataset_seleccionado == "Seleccionar dataset:":
        st.session_state.dataset_actual = None
        st.session_state.fecha_seleccion = None
        return

    # Detecta cambio de dataset
    if dataset_seleccionado != st.session_state.dataset_actual:
        st.session_state.dataset_actual = dataset_seleccionado
        st.session_state.fecha_seleccion = datetime.now()

    ruta = Path("processed_datasets") / st.session_state.dataset_actual

    if st.session_state.dataset_actual == "iadiza":
        separador = "\t"

    archivo_dataset = None

    for archivo in ruta.iterdir():
        if archivo.is_file():
            archivo_dataset = archivo

    nombre_dataset = st.session_state.dataset_actual.capitalize()
    cantidad_registros = lec.total_registros(archivo_dataset, separador)

    st.sidebar.success("### Dataset seleccionado")
    st.sidebar.info(f"""
                    **Nombre:** {nombre_dataset} \n
                    **Cantidad de registros:** {cantidad_registros} \n
                    **Fecha y hora de selección:**  
                    {st.session_state.fecha_seleccion.strftime('%d/%m/%Y | %H:%M:%S')} \n
                    """)
    

# Función 2.A - Ana Freitas
def mostrar_busqueda_texto_libre():
    """
    Se encarga de la interfaz de búsqueda por texto libre.
    Lee el dataset activo en la sesión y aplica el filtro reutilizando la función registrar_filtro (5.A) de la primera etapa.
    """
    # Verificamos que exista un dataset seleccionado en la sesión
    if "dataset_actual" not in st.session_state or st.session_state.dataset_actual is None or st.session_state.dataset_actual == "":
        st.warning("Por favor, seleccione un dataset válido en el menú lateral antes de continuar.")
        return

    nombre_dataset = st.session_state.dataset_actual
    
    # Determinamos el separador 
    separador_caracter = "\t" if nombre_dataset == "iadiza" else ","
    
    # Buscamos el archivo físico dentro de processed_datasets
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

    # Cargamos el DataFrame completo en memoria usando la función de la Etapa 1
    dataframe_completo = dataframe_dataset(archivo_encontrado, separador=separador_caracter)

    st.subheader("Búsqueda por texto libre")
    
    # 1. El usuario selecciona la columna  
    columnas_disponibles = dataframe_completo.columns.tolist()
    columna_seleccionada = st.selectbox(
        "Seleccione la columna por la que desea buscar:",
        options=columnas_disponibles
    )
    
    # 2. El usuario ingresa el valor que pretende encontrar 
    termino_busqueda = st.text_input(f"Ingrese el valor que pretende encontrar en '{columna_seleccionada}':").strip()
    
    # Si el usuario no escribió nada, mostramos el DataFrame completo tal como estaba originalmente
    if not termino_busqueda:
        return dataframe_completo

    # --- INTEGRACIÓN DEL EJERCICIO 5.A ---
    # Llamamos a registrar_filtro pasándole la ruta y los argumentos mediante **kwargs
    filas_filtradas_lista = act.registrar_filtro(
        path=str(archivo_encontrado), 
        c_delimiter=separador_caracter, 
        **{columna_seleccionada: termino_busqueda}
    )
    
    # Si la función encontró coincidencias, convertimos la lista de listas en DataFrame
    if filas_filtradas_lista:
        dataframe_filtrado = pd.DataFrame(filas_filtradas_lista, columns=columnas_disponibles)
        
        # Aplicamos la máscara case-insensitive y de subcadena requerida por el Ejercicio 2.A (Etapa 2)
        mascara_busqueda = dataframe_filtrado[columna_seleccionada].astype(str).str.contains(
            termino_busqueda, 
            case=False,   # Controla que sea case-insensitive
            na=False      # Descarta las celdas vacías
        )
        return dataframe_filtrado[mascara_busqueda]
    else:
        # Si no hubo ninguna coincidencia en el filtro, devolvemos un DataFrame vacío estructurado
        return pd.DataFrame(columns=columnas_disponibles)


# 2.b Fe Cordoba
def aplicar_filtros(
    df,
    nombres_cientificos=None,
    observador=None,
    paises=None,
    provincias=None,
    fecha_inicio=None,
    fecha_fin=None
):
    """Filtra el DataFrame según los parámetros de búsqueda seleccionados."""
    df_filtrado = df.copy()

    # Nombre científico
    if nombres_cientificos:

        df_filtrado = df_filtrado[
            df_filtrado["scientificName"].isin(nombres_cientificos)
        ]

    # Observador
    if observador:

        df_filtrado = df_filtrado[
            df_filtrado["recordedBy"]
            .astype(str)
            .str.contains(
                observador,
                case=False,
                na=False
            )
        ]

    nombre_dataset = st.session_state.dataset_actual
    if (nombre_dataset != 'xenocanto'):
        if paises:

          df_filtrado = df_filtrado[
             df_filtrado["countryCode"].isin(paises)
          ]
        if provincias:

         df_filtrado = df_filtrado[
             df_filtrado["stateProvince"].isin(provincias)
          ]
    else:
        if paises:
            patron_paises = "|".join(paises)
            df_filtrado = df_filtrado[df_filtrado['country'].str.contains(patron_paises, case=False, na=False)]

    # Fechas
    if "eventDate" in df_filtrado.columns:
        # Convertimos fila por fila a UTC de forma aislada
        df_filtrado["eventDate"] = df_filtrado["eventDate"].apply(
            lambda x: pd.to_datetime(x, errors="coerce", utc=True) if pd.notna(x) else pd.NaT
        )

        if fecha_inicio and fecha_fin:
            df_filtrado = df_filtrado[
                (
                    df_filtrado["eventDate"]
                    >= pd.to_datetime(fecha_inicio, utc=True)
                )
                &
                (
                    df_filtrado["eventDate"]
                    <= pd.to_datetime(fecha_fin, utc=True)
                )
            ]

    return df_filtrado

# Función 2.C - Agustin Garcia
COLUMNAS_RELEVANTES = {
    "iadiza": [
    "scientificName",
    "recordedBy",
    "eventDate",
    "stateProvince",
    "countryCode",
    "decimalLatitude",
    "decimalLongitude",
    "species",             
    "family",              
    "basisOfRecord",
    ],
    "inaturalist": [
    "scientificName",
    "inaturalistLogin", 
    "eventDate",
    "stateProvince",
    "countryCode",
    "decimalLatitude",
    "decimalLongitude",
    "taxonRank",
    "family",
    "captive", 
    ],
    "xenocanto": [
    "scientificName",
    "vernacularName",
    "recordedBy",
    "eventDate",
    "country",
    "locality",
    "latitudeDecimal",
    "longitudeDecimal",
    "behavior", 
    "sex",
    ]
}

REGISTROS_POR_PAGINA = 10 # Por convención


def mostrar_resultados(df_resultados, nombre_dataset):
    """
    Muestra los resultados de búsqueda con:
    - Cantidad de registros encontrados
    - Columnas relevantes con ordenamiento
    - Paginación
    - Detalle de registro
    """
    st.markdown(f"**Registros encontrados: {len(df_resultados)}**")

    if df_resultados.empty:
        st.info("No se encontraron registros con los criterios seleccionados.")
        return

    # Columnas relevantes
    columnas_presentes = hp.obtener_columnas_relevantes(nombre_dataset, df_resultados.columns.tolist(), COLUMNAS_RELEVANTES)
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

    df_pagina, inicio, fin, total_paginas = hp.paginar(df_vista, st.session_state.pagina_actual, REGISTROS_POR_PAGINA)

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

    opciones = {f"Registro #{inicio + i + 1}": df_pagina.iloc[i]["_index_original"] for i in range(len(df_pagina))}
    seleccion = st.selectbox("Ver detalle de un registro:", list(opciones.keys()), key="detalle_sel")

    index_original = opciones[seleccion]
    registro = df_resultados.loc[index_original]
    with st.expander(f"Detalle — {seleccion}", expanded=True):
        for campo, valor in registro.items():
            st.write(f"**{campo}:** {valor}")
                

#Funcion 2.D - Lucía Cipolla
def exportar_resultados (reg=None):
    """
        reg: Debe recibir lo que retorne mostrar_busqueda_texto_libre(). Puede ser un tipo DataFrame o None.
    """
    if (reg.empty):
        st.warning('No se puede importar un archivo vacío')
        return
    else:
        if (isinstance(reg,pd.DataFrame)):
            return reg.to_csv(index=False).encode('utf-8')
        else:
            st.warning('Ocurrió un problema inesperado')


