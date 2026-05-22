import csv
import os

from pathlib import Path

# ----------------------------------------- Gestión de archivos - funciones para lectura, apertura y rutas de datos. -----------------------------------------

# funcion de apoyo para las que crean/modifican processed datasets
def asegurar_directorio(ruta_archivo):
    """
    Crea las carpetas necesarias si no existen en el disco.
    """
    carpeta = os.path.dirname(ruta_archivo)
    os.makedirs(carpeta, exist_ok=True) 

# Funcion para encontrar la ruta raiz del proyecto 
def obtener_raiz_proyecto():
    """
    Encuentra la carpeta principal del proyecto.
    Usa la ubicación de este archivo como referencia para subir niveles 
    hasta la raíz y funciona en cualquier computadora.
    """
    return Path(__file__).parent.parent.absolute()


