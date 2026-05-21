from pathlib import Path
from datetime import datetime

import streamlit as st 
import pandas as pd

import src.utils as ut
import src.helpers as hp
import src.validaciones as va
import matplotlib.pyplot as plt


#funcion 1.a sofia martins
def dataframe_dataset(nombre,separador=','):
    dataframe=pd.read_csv(nombre,sep=separador,encoding='utf-8')
    return dataframe

#Funcion 1.b y C - Fe Cordoba, Agustin Garcia
def opcion_sidebar(separador=','):
    """Configura la barra lateral de Streamlit para la selección del dataset."""
    datasets = hp.obtener_nombres_datasets()
    if not datasets:
        st.sidebar.error("No hay datasets disponibles")
        return

    if "dataset_actual" not in st.session_state:
        st.session_state.dataset_actual = datasets[0]  # Inicializa session_state si no existe
    
    if "fecha_seleccion" not in st.session_state:
        st.session_state.fecha_seleccion = datetime.now() # Inicializa con la fechaactual si no existe

    dataset_actual = st.session_state.dataset_actual  # Obtiene dataset guardado en sesión

    indice_dataset = 0     # Para indice del dataset guardado (por defecto 0)

    if dataset_actual in datasets:
        indice_dataset = datasets.index(dataset_actual)

    # Crea selector
    dataset_seleccionado = st.sidebar.selectbox( 
        "Seleccione un dataset:",
        datasets,
        index=indice_dataset
    ) 

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

    nombre_dataset = st.session_state.dataset_actual.capitalize() # Inicia los nombres en mayúsculas
    cantidad_registros = ut.total_registros(archivo_dataset, separador)

    # Muestra en pantalla lo pedido en 1.C
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
    Lee el dataset activo en la sesión y aplica el filtro case-insensitive.
    """

    # Verificamos que exista un dataset seleccionado en la sesión
    if "dataset_actual" not in st.session_state:
        st.warning("Por favor, seleccione un dataset en el menú lateral.")
        return

    nombre_dataset = st.session_state.dataset_actual
    
    # Determinamos el separador 
    separador = "\t" if  nombre_dataset == "iadiza" else ","
    
    # Buscamos el archivo físico dentro de processed_datasets
    ruta_carpeta = Path("processed_datasets") /  nombre_dataset
    archivo = None
    
    if ruta_carpeta.exists():
        for archivo in ruta_carpeta.iterdir():
            if archivo.is_file():
                archivo = archivo
                break

    if not archivo:
        st.error("No se encontró el archivo de datos para este dataset.")
        return

    # Cargamos el DataFrame completo en memoria usando la función de la Etapa 1
    df = dataframe_dataset(archivo, separador=separador)

    st.subheader("Búsqueda por texto libre")
    
    # 1. El usuario selecciona la columna  
    columnas_disponibles = df.columns.tolist()
    columna_seleccionada = st.selectbox(
        "Seleccione la columna por la que desea buscar:",
        options=columnas_disponibles
    )
    
    # 2. El usuario ingresa el valor que pretende encontrar 
    termino_busqueda = st.text_input(f"Ingrese el valor que pretende encontrar en '{columna_seleccionada}':")
    
    # Aplicamos el filtro solo si el usuario escribió algo
    if termino_busqueda:
         # astype(str) evita errores si la columna tiene números o nulos
        mascara = df[columna_seleccionada].astype(str).str.contains(
            termino_busqueda, 
            case=False,   # case=False maneja case-insensitive
            na=False  # na=False descarta las filas vacías (NaN)
        )
        df_filtrado = df[mascara]
    else:
        df_filtrado = df.copy()

    # Retornamos el dataframe filtrado para que pueda ser usado en los siguientes ejercicios
    return df_filtrado


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


# --- EJERCICIO 3.A: Gráfico de Barras Dinámico ---
def graficar_registros_por_ubicacion():
    """
    Genera un gráfico de barras por país o por provincia según los datos disponibles.
    """

    if "dataset_actual" not in st.session_state:
        st.warning("Por favor, seleccione un dataset en el menú lateral.")
        return

    dataset_nombre = st.session_state.dataset_actual
    separador = "\t" if dataset_nombre == "iadiza" else ","
    
    ruta_carpeta = Path("processed_datasets") / dataset_nombre
    archivo = None
    if ruta_carpeta.exists():
        for archivo in ruta_carpeta.iterdir():
            if archivo.is_file():
                archivo = archivo
                break

    if not archivo:
        st.error("No se encontró el archivo de datos.")
        return

    df = dataframe_dataset(archivo, separador=separador)

    st.subheader("Distribución geográfica de registros")

    # Mapeo de columnas a minúsculas para evitar problemas de formato
    columnas_mapeadas = {col.lower(): col for col in df.columns}
    col_pais = columnas_mapeadas.get('country') 
    col_provincia = columnas_mapeadas.get('stateprovince') or columnas_mapeadas.get('locality')

    # Si la columna 'country' EXISTE en el archivo
    if col_pais:
        df[col_pais] = df[col_pais].astype(str).str.strip()
        df_limpio = df[~df[col_pais].isin(['nan', '', 'None'])]
        paises_unicos = df_limpio[col_pais].unique()
        cantidad_paises = len(paises_unicos)
    else:
        # Si NO existe la columna 'country', asumimos que es un solo país implícito
        cantidad_paises = 1
        paises_unicos = ["No especificado (País Único)"]

    # --- CASO A: El dataset explícitamente tiene más de un país ---
    if cantidad_paises > 1:
        st.info(f"El dataset contiene registros de {cantidad_paises} países.")
        
        n_paises = st.slider(
            "Seleccione cuántos países desea visualizar (los N más frecuentes):",
            min_value=1,
            max_value=int(cantidad_paises),
            value=min(5, int(cantidad_paises))
        )
        
        datos_grafico = df_limpio[col_pais].value_counts().head(n_paises)
        titulo_grafico = f"Top {n_paises} de registros por País"
        etiqueta_x = "País"

    # --- CASO B: Un solo país (o no tiene la columna 'country' pero queremos ver provincias) ---
    elif cantidad_paises == 1:
        pais_actual = paises_unicos[0]
        
        if col_pais:
            st.info(f"Todos los registros pertenecen a un único país: **{pais_actual}**")
        else:
            st.info("El dataset no especifica columna de país. Se organiza directamente por ubicación regional.")
        
        if not col_provincia:
            st.warning("No se encontraron columnas de provincia o localidad ('stateProvince' / 'locality') para este dataset.")
            return
            
        # Limpiamos y extraemos las provincias/localidades más frecuentes
        df[col_provincia] = df[col_provincia].astype(str).str.strip()
        df_prov_filtrado = df[~df[col_provincia].isin(['nan', '', 'None'])]
        
        datos_grafico = df_prov_filtrado[col_provincia].value_counts().head(15) 
        titulo_grafico = f"Top 15 de registros por Provincia/Localidad"
        etiqueta_x = "Provincia / Localidad"
    else:
        st.warning("No hay registros válidos para graficar.")
        return

    if not datos_grafico.empty:
        # Invertimos el orden de los datos para que el más grande quede arriba en el gráfico horizontal
        datos_ordenados = datos_grafico.iloc[::-1]
        
        # Creamos la figura y el gráfico
        figura, grafico = plt.subplots(figsize=(10, 6)) # Un poco más alto para dar aire entre filas
        
        # CAMBIO CLAVE: Usamos 'barh' en lugar de 'bar' para hacer las barras horizontales
        datos_ordenados.plot(kind='barh', ax=grafico, color='skyblue', edgecolor='black')
        
        # Configuramos los títulos y etiquetas (¡Ojo! Los ejes se invierten)
        grafico.set_title(titulo_grafico, fontsize=12, fontweight='bold')
        grafico.set_xlabel("Cantidad de Registros", fontsize=10) # Ahora la cantidad está abajo
        grafico.set_ylabel(etiqueta_x, fontsize=10)             # El nombre geográfico está al costado
        
        # Ajustamos el tamaño de la letra de los nombres para que quepan bien
        grafico.tick_params(axis='y', labelsize=9)
        
        # Dejamos espacio a la izquierda para que los nombres largos no se corten
        figura.subplots_adjust(left=0.3, right=0.95, top=0.9, bottom=0.1) 
        
        # Mostramos en Streamlit
        st.pyplot(figura)
        plt.close(figura)