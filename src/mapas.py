from streamlit_folium import st_folium

import folium
import pandas as pd
import streamlit as st

import src.validaciones as va
from src.web_manager import COLUMNAS_RELEVANTES

def mostrar_mapa_interactivo(df_busqueda):
    total_inicial = len(df_busqueda)
    
    if total_inicial == 0:
        st.info("El dataset de búsqueda está vacío.")
        return

    # Filtramos los datos usando la función corregida
    mascara = df_busqueda.apply(va.es_coordenada_valida, axis=1)
    df_mapa = df_busqueda[mascara].copy()
    
    registros_excluidos = total_inicial - len(df_mapa)
    
    if registros_excluidos > 0:
        st.warning(f"ℹ️ Se excluyeron **{registros_excluidos}** registros del mapa por poseer coordenadas inválidas o nulas.")
    else:
        st.success("✅ Todos los registros poseen coordenadas válidas.")

    st.subheader("Mapa Interactivo")
    

    # Mapeamos las opciones legibles con los nombres reales de las columnas, adaptado a los encabezados de los 3 datasets
    columnas_posibles = {
        'Especie': ['scientificName', 'species', 'genus'],
        'País': ['country', 'countryCode'],
        'Institución': ['institutionCode', 'collectionCode']
    }

    opciones_criterio = {}
    for legible, lista_campos in columnas_posibles.items():
        # Buscamos cuál de los nombres posibles existe realmente en el dataset actual
        for campo in lista_campos:
            if campo in df_mapa.columns:
                opciones_criterio[legible] = campo
                break  # Encontró uno, pasa al siguiente criterio

    columna_color = None

    if opciones_criterio:
        criterio_elegido = st.selectbox("Seleccione el criterio para colorear los puntos:", list(opciones_criterio.keys()))
        columna_color = opciones_criterio[criterio_elegido]

    # Lista de colores estables que soporta Folium nativamente
    colores_disponibles = ['blue', 'green', 'red', 'purple', 'orange', 'darkred', 'lightred', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'lightblue', 'lightgreen', 'gray', 'black']

    # Identificamos los nombres reales de las columnas en el dataset
    col_lat = 'decimalLatitude' if 'decimalLatitude' in df_mapa.columns else 'latitudeDecimal'
    col_lon = 'decimalLongitude' if 'decimalLongitude' in df_mapa.columns else 'longitudeDecimal'
    
    # Convertimos a float para que Folium pueda graficar
    df_mapa[col_lat] = df_mapa[col_lat].astype(float)
    df_mapa[col_lon] = df_mapa[col_lon].astype(float)

    if len(df_mapa) > 0:
        # Si el usuario NO filtró nada, recortamos a 100 primeros
        # Si filtró un registro específico, entra directo al else sin recortar.
        MAX_PUNTOS = 100
        if len(df_mapa) > MAX_PUNTOS:
            st.info(f"💡 Mostrando los primeros {MAX_PUNTOS} registros.")
            df_render = df_mapa.head(MAX_PUNTOS)
        else:
            df_render = df_mapa
        
        # Creamos el mapa centrado en el promedio geográfico de los puntos a mostrar
        centro_lat = df_render[col_lat].mean()
        centro_lon = df_render[col_lon].mean()
        mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=4)
        
        # Asignar los colores únicos según las categorías del criterio
        mapeo_colores = {}
        if columna_color:
            categorias_unicas = df_render[columna_color].unique().tolist()
            for contador, categoria in enumerate(categorias_unicas):
                mapeo_colores[categoria] = colores_disponibles[contador % len(colores_disponibles)]

      # Dibujamos sobre df_render
        for indice, fila in df_render.iterrows():
            # Buscamos el valor real usando .get() encadenado
            valor_especie = fila.get('scientificName') or fila.get('species') or fila.get('genus') or 'No disponible'
            valor_pais = fila.get('country') or fila.get('countryCode') or 'No disponible'
            valor_institucion = fila.get('institutionCode') or fila.get('collectionCode') or 'No disponible'

            info_popup = (
                f"<b>Especie:</b> {valor_especie}<br>"
                f"<b>País:</b> {valor_pais}<br>"
                f"<b>Institución:</b> {valor_institucion}"
            )

            # determinar el color
            color_marcador = 'blue'  # Color base por defecto
            if columna_color:
                valor_fila = fila[columna_color]
                color_marcador = mapeo_colores.get(valor_fila, 'blue')

            folium.Marker(
                location=[fila[col_lat], fila[col_lon]],
                popup=folium.Popup(info_popup, max_width=300),
                icon=folium.Icon(color=color_marcador, icon="info-sign")  # <--- Usamos la variable dinámica
            ).add_to(mapa)
            
        mapa_data = st_folium(mapa, width=1100, height=500)

        if mapa_data and mapa_data.get("last_object_clicked"):
            st.session_state.punto_seleccionado = mapa_data["last_object_clicked"]


# Ejercicio 6.C - Agustin Garcia

TRADUCCION_COLUMNAS = {
    "scientificName":   "Nombre científico",
    "recordedBy":       "Observador",
    "eventDate":        "Fecha",
    "stateProvince":    "Provincia",
    "countryCode":      "País",
    "country":          "País",
    "decimalLatitude":  "Latitud",
    "decimalLongitude": "Longitud",
    "latitudeDecimal":  "Latitud",
    "longitudeDecimal": "Longitud",
    "species":          "Especie",
    "family":           "Familia",
    "basisOfRecord":    "Tipo de registro",
    "inaturalistLogin": "Usuario iNaturalist",
    "taxonRank":        "Rango taxonómico",
    "captive":          "¿Cautivo?",
    "vernacularName":   "Nombre común",
    "locality":         "Localidad",
    "behavior":         "Comportamiento",
    "sex":              "Sexo",
}

def mostrar_ficha_registro(df_busqueda, nombre_dataset):
    """
    Muestra una ficha con la información taxonómica, lugar y fecha
    del registro seleccionado en el mapa.
    """

    punto = st.session_state.get("punto_seleccionado")

    if not punto:
        st.info("Seleccioná un punto en el mapa para ver su ficha.")
        return

    col_lat = "decimalLatitude" if "decimalLatitude" in df_busqueda.columns else "latitudeDecimal"
    col_lon = "decimalLongitude" if "decimalLongitude" in df_busqueda.columns else "longitudeDecimal"

    lat = punto.get("lat")
    lon = punto.get("lng")

    coincidencias = df_busqueda[
        (df_busqueda[col_lat].astype(float) == lat) &
        (df_busqueda[col_lon].astype(float) == lon)
    ]

    if coincidencias.empty:
        st.warning("No se encontró el registro seleccionado.")
        return

    registro = coincidencias.iloc[0]
    columnas_ficha = COLUMNAS_RELEVANTES.get(nombre_dataset, [])

    st.markdown("---")
    st.subheader("Ficha del registro")

    ficha = {
        TRADUCCION_COLUMNAS.get(campo, campo): registro[campo]
        for campo in columnas_ficha
        if campo in registro.index and pd.notna(registro[campo]) and str(registro[campo]).strip() != ""
    }

    df_ficha = pd.DataFrame(ficha.items(), columns=["Campo", "Valor en el registro"])
    st.table(df_ficha)
