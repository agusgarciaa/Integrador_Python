from pathlib import Path
from datetime import datetime

import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

import src.utils as ut
import src.helpers as hp
import src.validaciones as va


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
    cantidad_registros = ut.total_registros(archivo_dataset, separador)

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
    if "dataset_actual" not in st.session_state or st.session_state.dataset_actual is None or st.session_state.dataset_actual == "":
        st.warning("Por favor, seleccione un dataset válido en el menú lateral antes de continuar.")
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


# --- EJERCICIO 3.A: Gráfico de Barra ---
def graficar_registros_por_ubicacion():
    """
    Genera un gráfico de barras por país o por provincia según los datos disponibles.
    """

    if "dataset_actual" not in st.session_state or st.session_state.dataset_actual is None or st.session_state.dataset_actual == "":
        st.warning("Por favor, seleccione un dataset válido en el menú lateral antes de continuar.")
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


# --- EJERCICIO 4.A: Formuario ---
def insertar_nuevo_registro():
    """
    Crea un formulario dinámico para ingresar un nuevo registro en el dataset activo, validando los campos y guardando los cambios.
    """
    if "dataset_actual" not in st.session_state or st.session_state.dataset_actual is None or st.session_state.dataset_actual == "":
        st.warning("Por favor, seleccione un dataset válido en el menú lateral antes de continuar.")
        return

    # Ahora es 100% seguro obtener el nombre porque sabemos que no es None
    dataset_nombre = st.session_state.dataset_actual
    
    # Si el dataset es 'iadiza', usamos tabulador (\t), de lo contrario usamos coma (,)
    separador = "\t" if dataset_nombre.lower() == "iadiza" else "," 
    
    # Construye la ruta de forma segura sin peligro de TypeError
    ruta_carpeta = Path("processed_datasets") / dataset_nombre 
    archivo_target = None

    if ruta_carpeta.exists():
        for archivo in ruta_carpeta.iterdir():
            if archivo.is_file():
                archivo_target = archivo
                break

    if not archivo_target:
        st.error("No se encontró el archivo de datos.")
        return

    # Carga el DataFrame actual (Ejercicio 1.A)
    df = dataframe_dataset(archivo_target, separador=separador)

    st.subheader(f"Insertar registro en: {dataset_nombre.capitalize()}")

    # 2. DEFINICIÓN DE ATRIBUTOS PRINCIPALES: Seleccionamos las columnas clave del estándar Darwin Core
    # Esto evita abrumar al usuario si el dataset tiene 50 columnas, mostrando solo las más importantes
    columnas_clave = ['scientificname', 'eventdate', 'country', 'stateprovince', 'locality', 'recordedby', 'individualcount']
    
    # Filtramos las columnas reales del dataset que coincidan con nuestros atributos principales
    campos_formulario = [col for col in df.columns if col.lower() in columnas_clave]

    # Si por alguna razón no coincide ninguna, usamos las primeras 5 columnas por defecto
    if not campos_formulario:
        campos_formulario = df.columns.tolist()[:5]

    # 3. CREACIÓN DEL FORMULARIO DE STREAMLIT (st.form)
    # Usar st.form es obligatorio para que la página no se recargue con cada letra que escribe el usuario
    with st.form(key="formulario_insercion"):
        st.write("Complete los datos del nuevo registro:")
        
        # Diccionario para almacenar lo que el usuario escribe en cada campo
        datos_ingresados = {}
        
        # Generamos los campos de entrada de forma dinámica recorriendo la lista
        for campo in campos_formulario:
            # Si la columna es de tipo numérico (como conteo de individuos), usamos un input numérico
            if df[campo].dtype in ['int64', 'float64']:
                datos_ingresados[campo] = st.number_input(f"{campo}:", min_value=0, value=0)
            else:
                # Para texto libre (nombres, fechas, localidades) usamos entrada de texto común
                datos_ingresados[campo] = st.text_input(f"{campo}:", value="")
        
        # Botón de envío obligatorio dentro de todo st.form
        boton_enviar = st.form_submit_button(label="Confirmar Inserción")

    # 4. PROCESAMIENTO Y VALIDACIÓN AL HACER CLICK EN EL BOTÓN
    if boton_enviar:
        # Bandera para controlar si todo el formulario es válido
        formulario_valido = True
        
        # REQUERIMIENTO: Mostrar mensajes de error específicos por campo (Ejercicio 4.A)
        for campo, valor in datos_ingresados.items():
            # Validación básica local: verificar que no se envíen campos obligatorios vacíos
            if str(valor).strip() == "":
                st.error(f"El campo '{campo}' no puede estar vacío.")
                formulario_valido = False
    

        if not va.validar(**datos_ingresados):
            st.error("La validación de la estructura o consistencia de datos ha fallado.")
            formulario_valido = False

        # 5. INSERCIÓN REAL Y PERSISTENCIA (Si todo es válido)
        if formulario_valido:
            try:
                # Convertimos el diccionario de datos ingresados en un nuevo DataFrame de una sola fila
                nuevo_registro_df = pd.DataFrame([datos_ingresados])
                
                # Concatenamos (añadimos) el nuevo registro al DataFrame original
                df_actualizado = pd.concat([df, nuevo_registro_df], ignore_index=True)
                
                # Guardamos el DataFrame actualizado sobrescribiendo el archivo en processed_datasets
                df_actualizado.to_csv(archivo_target, sep=separador, index=False, encoding='utf-8')
                
                # REQUERIMIENTO: Informar al usuario sobre el resultado exitoso
                st.success("¡Registro insertado con éxito en el dataset!")
                
                # ut.registrar_operacion("INSERT", dataset_nombre, "Éxito: Registro añadido manualmente")
                
                # Forzamos a Streamlit a limpiar el formulario mostrando los datos actualizados
                st.balloons()
                
            except Exception as un_error:
                # Si algo falla en la escritura o procesamiento, informamos el error y lo registramos en el log
                st.error(f"Error crítico al insertar el registro: {un_error}")
                # ut.registrar_operacion("ERROR", dataset_nombre, f"Fallo en INSERT: {un_error}")