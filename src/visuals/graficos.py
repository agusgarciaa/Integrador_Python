import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

import src.operaciones.lecturas as lc

# Función 3.A (segunda parte)- Ana Freitas
def graficar_registros_por_ubicacion(df):
    """
    Genera un gráfico de barras por país o por provincia según los datos disponibles,
    unificando criterios de nombres de países (como AR y Argentina).
    """

    columnas_mapeadas = {col.lower(): col for col in df.columns}
    col_pais = columnas_mapeadas.get('country') or columnas_mapeadas.get('countrycode')
    col_provincia = columnas_mapeadas.get('stateprovince') or columnas_mapeadas.get('locality')

    if col_pais:
        # Limpieza inicial básica
        df[col_pais] = df[col_pais].astype(str).str.strip()
        df_limpio = df[~df[col_pais].isin(['nan', '', 'None'])].copy()
        df_limpio[col_pais] = df_limpio[col_pais].str.upper()
        df_limpio[col_pais] = df_limpio[col_pais].replace(['AR', 'ARG'], 'ARGENTINA')
        
        paises_unicos = df_limpio[col_pais].unique()
        cantidad_paises = len(paises_unicos)
    else:
        cantidad_paises = 1
        paises_unicos = ["No especificado (País Único)"]

    if cantidad_paises > 1:
        st.info(f"El dataset contiene registros de {cantidad_paises} países.")
        
        n_paises = st.slider(
            "Seleccione cuántos países desea visualizar:",
            min_value=1,
            max_value=int(cantidad_paises),
            value=min(5, int(cantidad_paises)),
            key="slider_paises_ubicacion"
        )
        
        datos_grafico = df_limpio[col_pais].value_counts().head(n_paises)
        titulo_grafico = f"Top {n_paises} de registros por País"
        etiqueta_x = "País"

    elif cantidad_paises == 1:
        pais_actual = paises_unicos[0]
        
        if col_pais:
            st.info(f"Todos los registros pertenecen a un único país: **{pais_actual.capitalize()}**")
        else:
            st.info("El dataset no especifica columna de país. Se organiza directamente por ubicación regional.")
        
        if not col_provincia:
            st.warning("No se encontraron columnas de provincia o localidad para este dataset.")
            return
            
        df[col_provincia] = df[col_provincia].astype(str).str.strip()
        df_prov_filtrado = df[~df[col_provincia].isin(['nan', '', 'None'])]
        
        datos_grafico = df_prov_filtrado[col_provincia].value_counts().head(15) 
        titulo_grafico = "Top 15 de registros por Provincia/Localidad"
        etiqueta_x = "Provincia / Localidad"
    else:
        st.warning("No hay registros válidos para graficar.")
        return

    if not datos_grafico.empty:
        datos_ordenados = datos_grafico.iloc[::-1]
        
        figura, grafico = plt.subplots(figsize=(10, 6))
        
        datos_ordenados.plot(kind='barh', ax=grafico, color='skyblue', edgecolor='black')
        
        grafico.set_title(titulo_grafico, fontsize=12, fontweight='bold')
        grafico.set_xlabel("Cantidad de Registros", fontsize=10)
        grafico.set_ylabel(etiqueta_x, fontsize=10)
        grafico.tick_params(axis='y', labelsize=9)
        
        figura.subplots_adjust(left=0.3, right=0.95, top=0.9, bottom=0.1) 
        
        st.pyplot(figura)
        plt.close(figura)


# Función 3.C - Agustin Garcia
def graficar_distribucion_taxonomica(df, nombre_dataset):
    """
    Muestra un gráfico de barras con la distribución de registros
    por nivel taxonómico (clase, orden o familia).
    """

    COLUMNAS_TAXONOMICAS = {
        "iadiza":      {"Clase": "class", "Orden": "order", "Familia": "family"},
        "inaturalist": {"Clase": "class", "Orden": "order", "Familia": "family"},
        "xenocanto":   {"Familia": "family"},
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

    conteo = df[columna].replace("", pd.NA).dropna().value_counts().head(20)  

    if conteo.empty:
        st.info("No hay datos disponibles para el nivel seleccionado.")
        return
    
    if nombre_dataset == 'xenocanto':
        st.info("Xenocanto solo posee el nivel taxonómico 'Familia'")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(conteo.index, conteo.values, color="steelblue")
    ax.set_title(f"Distribución por {nivel} — Top {len(conteo)}")
    ax.set_xlabel(nivel)
    ax.set_ylabel("Cantidad de registros")
    plt.xticks(rotation=45, ha="right")  
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


# Funcion 3.D - Fe Cordoba
def graficar_porcentaje_nulos(nombre_dataset, archivo):
    """Crea un grafico de barras horizontales de los valores no nulos por columna."""

    if(nombre_dataset == "iadiza"):
        separador = "\t"
    else:
       separador = ","
    diccionario_nulos = lc.porcentaje_nulos(archivo,separador)

    serie_nulos = pd.Series(diccionario_nulos)

    serie_no_nulos = 100.0 - serie_nulos

    serie_ordenada = serie_no_nulos.sort_values(ascending=True)

    if(nombre_dataset == "iadiza"):
        ax = serie_ordenada.plot(
        kind='barh',
        figsize=(12, 30)
        )
    else:
        ax = serie_ordenada.plot(
        kind='barh',
        figsize=(12, 12)
        )

    ax.set_title("Porcentaje de valores no nulos por columna")

    ax.set_xlabel("Porcentaje")
    ax.set_ylabel("Columnas")

    ax.tick_params(axis='y', labelsize=6)

    plt.tight_layout()

    fig = ax.get_figure()

    st.pyplot(fig)
