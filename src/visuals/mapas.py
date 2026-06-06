from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

import folium
import pandas as pd
import streamlit as st

import src.utils.constantes as const
import src.operaciones.validaciones as va


def mostrar_mapa_interactivo(df_busqueda):
    """
    Genera y renderiza un mapa interactivo con Folium utilizando los registros filtrados.
    
    Filtra coordenadas válidas, aplica colores según el criterio seleccionado,
    agrupa marcadores y captura los clics del usuario en el mapa.
    """
    
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
    
    columnas_posibles = {
        'Especie': ['scientificName', 'species', 'genus'],
        'País': ['country', 'countryCode'],
        'Institución': ['institutionCode', 'collectionCode']
    }

    opciones_criterio = {}
    for legible, lista_campos in columnas_posibles.items():
        for campo in lista_campos:
            if campo in df_mapa.columns:
                opciones_criterio[legible] = campo
                break  

    columna_color = None

    if opciones_criterio:
        criterio_elegido = st.selectbox("Seleccione el criterio para colorear los puntos:", list(opciones_criterio.keys()))
        columna_color = opciones_criterio[criterio_elegido]

    colores_disponibles = ['blue', 'green', 'red', 'purple', 'orange', 'darkred', 'lightred', 'darkblue', 'darkgreen', 'cadetblue', 
                           'darkpurple', 'pink', 'lightblue', 'lightgreen', 'gray', 'black']

    col_lat = 'decimalLatitude' if 'decimalLatitude' in df_mapa.columns else 'latitudeDecimal'
    col_lon = 'decimalLongitude' if 'decimalLongitude' in df_mapa.columns else 'longitudeDecimal'
    
    df_mapa[col_lat] = df_mapa[col_lat].astype(float)
    df_mapa[col_lon] = df_mapa[col_lon].astype(float)

    if len(df_mapa) > 0:
        MAX_PUNTOS = 100
        if len(df_mapa) > MAX_PUNTOS:
            st.info(f"💡 Mostrando los primeros {MAX_PUNTOS} registros.")
            df_render = df_mapa.head(MAX_PUNTOS)
        else:
            df_render = df_mapa 
        
        centro_lat = df_render[col_lat].mean()
        centro_lon = df_render[col_lon].mean()

        mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=4, tiles=None)

        folium.raster_layers.TileLayer(
            tiles="https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{y}.png",
            attr="Instituto Geográfico Nacional (IGN) - República Argentina",
            name="Argenmap (IGN)",
            overlay=False,
            control=True,
            tms=True  
        ).add_to(mapa)

        usar_cluster = len(df_render) > 10
        if usar_cluster:
            contenedor_puntos = MarkerCluster().add_to(mapa)
        else:
            contenedor_puntos = mapa
        
        mapeo_colores = {}
        if columna_color:
            categorias_unicas = df_render[columna_color].unique().tolist()
            for contador, categoria in enumerate(categorias_unicas):
                mapeo_colores[categoria] = colores_disponibles[contador % len(colores_disponibles)]

        for indice, fila in df_render.iterrows():
            valor_id = str(fila.get('id', '') or fila.get('gbifID', '') or fila.get('occurrenceID', '')).strip()
            valor_especie = fila.get('scientificName') or fila.get('species') or fila.get('genus') or 'No disponible'
            valor_pais = fila.get('country') or fila.get('countryCode') or 'No disponible'
            valor_institucion = fila.get('institutionCode') or fila.get('collectionCode') or 'No disponible'

            info_popup = (
                f"<b>Especie:</b> {valor_especie}<br>"
                f"<b>País:</b> {valor_pais}<br>"
                f"<b>Institución:</b> {valor_institucion}"
            )

            color_marcador = 'blue'
            if columna_color:
                valor_fila = fila[columna_color]
                color_marcador = mapeo_colores.get(valor_fila, 'blue')

            folium.Marker(
                location=[fila[col_lat], fila[col_lon]],
                popup=folium.Popup(info_popup, max_width=300),
                tooltip=valor_id,
                icon=folium.Icon(color=color_marcador, icon="info-sign") 
            ).add_to(contenedor_puntos) 
            
        id_primer_registro = df_render.iloc[0].get('id', 0) if len(df_render) > 0 else 0
        mapa_key = f"mapa_folium_dinamico_{len(df_render)}_{id_primer_registro}"

        mapa_data = st_folium(
            mapa, 
            width=1100, 
            height=500,
            key=mapa_key
        )
        if mapa_data and mapa_data.get("last_object_clicked_tooltip"):
            tooltip_actual = mapa_data["last_object_clicked_tooltip"]
    
            if st.session_state.get("_ultimo_tooltip") != tooltip_actual:
                st.session_state.punto_seleccionado = mapa_data["last_object_clicked"]
                st.session_state.id_multimedia = tooltip_actual
                st.session_state._ultimo_tooltip = tooltip_actual
        else:
            st.session_state._ultimo_tooltip = None

def mostrar_ficha_registro(df_busqueda, nombre_dataset):
    """
    Muestra una ficha con la información taxonómica, lugar y fecha
    del registro seleccionado en el mapa.
    """

    punto = st.session_state.get("punto_seleccionado")
    id_seleccionado = st.session_state.get("id_multimedia")

    if not punto and not id_seleccionado:
        st.info("Seleccioná un punto en el mapa para ver su ficha.")
        return

    if id_seleccionado:
        col_id = next((c for c in ["id", "gbifID", "occurrenceID", "catalogNumber"] if c in df_busqueda.columns), None)
        if col_id:
            coincidencias = df_busqueda[df_busqueda[col_id].astype(str) == str(id_seleccionado)]

    if not id_seleccionado or coincidencias.empty:
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
    columnas_ficha = const.COLUMNAS_FICHA.get(nombre_dataset, [])

    st.markdown("---")
    st.subheader("Ficha del registro")

    ficha = {
        const.TRADUCCION_COLUMNAS.get(campo, campo): registro[campo]
        for campo in columnas_ficha
        if campo in registro.index and pd.notna(registro[campo]) and str(registro[campo]).strip() != ""
    }

    df_ficha = pd.DataFrame(ficha.items(), columns=["Campo", "Valor en el registro"])
    df_ficha["Valor en el registro"] = df_ficha["Valor en el registro"].astype(str)
    st.table(df_ficha)

    return registro
