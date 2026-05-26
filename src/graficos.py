from pathlib import Path

import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

import src.web_manager as wm

# Función 3.A (segunda parte)- Ana Freitas
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

    df = wm.dataframe_dataset(archivo, separador=separador)

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


# Función 3.C - Agustin Garcia
def grafico_distribucion_taxonomica(df, nombre_dataset):
    """
    Muestra un gráfico de barras con la distribución de registros
    por nivel taxonómico (clase, orden o familia).
    """

    COLUMNAS_TAXONOMICAS = {
        "iadiza":      {"Clase": "class", "Orden": "order", "Familia": "family"},
        "inaturalist": {"Clase": "class", "Orden": "order", "Familia": "family"},
        "xenocanto":   {"Familia": "family"},  # xenocanto no tiene class ni order
    }
    
    columnas = COLUMNAS_TAXONOMICAS.get(nombre_dataset, {})
    if not columnas:
        st.info("El dataset no cuenta con columnas taxonómicas disponibles.")
        return

    nivel = st.selectbox("Nivel taxonómico:", list(columnas.keys()), key="selector_taxonomia")
    columna = columnas[nivel]

    if columna not in df.columns:
        st.warning(f"El dataset no contiene la columna '{columna}'.")
        return

    # Contar registros por nivel, ignorando vacíos
    conteo = df[columna].replace("", pd.NA).dropna().value_counts().head(20)  # se limita a los 20 más frecuentes y descarta filas con valor vacío

    if conteo.empty:
        st.info("No hay datos disponibles para el nivel seleccionado.")
        return
    
    if nombre_dataset == 'xenocanto':
        st.info("Xenocanto solo posee el nivel taxonómico 'Familia'")

    # Grafico
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(conteo.index, conteo.values, color="steelblue")
    ax.set_title(f"Distribución por {nivel} — Top {len(conteo)}")
    ax.set_xlabel(nivel)
    ax.set_ylabel("Cantidad de registros")
    plt.xticks(rotation=45, ha="right")  # rotado a 45 grados para no pisar los valores al mostrar la información. 
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)  # libera memoria
