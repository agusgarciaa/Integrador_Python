from pathlib import Path

import streamlit as st
import pandas as pd

def mostrar_multimedia(nombre_dataset):
    id_mapa = st.session_state.get("id_multimedia")

    if not id_mapa:
        return
    
    id_mapa = str(id_mapa).strip()

    if nombre_dataset.lower() == 'iadiza':
        return
    if nombre_dataset.lower() == 'inaturalist':
        ruta_multimedia = Path('raw_datasets') / 'inaturalist' / 'media.csv'
        columna_id = 'id'
        columna_url = 'identifier'
        separador = ','
    elif nombre_dataset.lower() == 'xenocanto':
        ruta_multimedia = Path('raw_datasets') / 'xenocanto' / 'Multimedia.txt'
        columna_id = 'coreid'
        columna_url = 'identifier'
        separador = ','

    try:
        df_multimedia = pd.read_csv(ruta_multimedia,delimiter=separador,dtype={columna_id: str})
        df_multimedia.columns = df_multimedia.columns.str.strip().str.lower()

        coincidencias = df_multimedia[df_multimedia[columna_id].astype(str)==id_mapa]
        if coincidencias.empty:
            st.info('No se encontró multimedia para este registro')
            return
    except FileNotFoundError:
        st.error(f'No se pudo encontrar el archivo en {ruta_multimedia}')
        return
    
    if nombre_dataset.lower() == 'inaturalist':
        columnas = st.columns(3)
        fotos_validas = 0
        for i,fila in coincidencias.iterrows():
            url_foto = fila.get(columna_url)
            url_foto_txt = str(fila.get(columna_url))
            if pd.notna(url_foto) and (url_foto_txt.startswith('http')):
                col = columnas[fotos_validas % 3]
                fotos_validas += 1
                col.image(url_foto_txt, use_container_width=True)
        if fotos_validas == 0:
            st.info('El registro existe pero no se pudo recuperar el enlace')
    elif nombre_dataset.lower() == 'xenocanto':
        audios_validos = 0
        for i,fila in coincidencias.iterrows():
            url_audio = fila.get(columna_url, '')
            url_audio_txt = str(fila.get(columna_url, '')).strip().lower()
            formato = str(fila.get('type', ''))
            if (formato.lower() == 'sound') and (pd.notna(url_audio)) and (url_audio_txt.startswith('http')):
                st.audio(url_audio_txt)
                audios_validos += 1
        if audios_validos == 0:
            st.info('El registro existe pero no se pudo recuperar el enlace')