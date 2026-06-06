import streamlit as st 

import src.utils.rutas as rut
import src.visuals.est_sistema as est


st.title("Logs generados.")
ruta = rut.obtener_ruta_log("logs", "operations.log")

# 4.E - Fe Cordoba
est.filtrar_logs(ruta)

# 8.C - Fe Cordoba
est.logs_tabulados(ruta)