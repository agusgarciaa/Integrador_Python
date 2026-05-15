import streamlit as st
import src.webmanager as wb 



wb.opcion_sidebar()
dataset = st.session_state.dataset_actual
