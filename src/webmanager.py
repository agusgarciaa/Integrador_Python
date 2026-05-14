from pathlib import Path
import os

import streamlit as st 
import src.utils as ut
import pandas as pd

#funcion 1.a sofia martins
def Dataframe_dataset(nombre,separador=','):
    dataframe=pd.read_csv(nombre,sep=separador,encoding='utf-8')
    return dataframe