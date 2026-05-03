import csv

from pathlib import Path

# ----------------------------------------- Gestión de archivos - funciones para lectura, apertura y rutas de datos. -----------------------------------------

# Funcion para encontrar la ruta raiz del proyecto - Ana Freitas
def obtener_raiz_proyecto():
    """
    Encuentra la carpeta principal del proyecto.
    Usa la ubicación de este archivo como referencia para subir niveles 
    hasta la raíz y funciona en cualquier computadora.
    """
    return Path(__file__).parent.parent.absolute()


