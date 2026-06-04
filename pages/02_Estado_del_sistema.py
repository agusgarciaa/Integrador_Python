from pathlib import Path
import os
import csv
import streamlit as st 
import pandas as pd
import src.utils.web_manager as wb 
import src.utils.rutas as rut
import src.visuals.est_sistema as est


st.set_page_config(page_title="Estado del Sistema- Logs", layout="wide")
st.title("Logs generados.")
ruta = rut.obtener_ruta_log("logs", "operations.log")

# 4.E - Fe Cordoba
est.filtrar_logs(ruta)

# 8.C - Fe Cordoba
est.logs_tabulados(ruta)