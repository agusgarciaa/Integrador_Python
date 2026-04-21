import csv
import sys
import os
from src.file_manager import get_columns_names

sys.path.append(os.path.abspath(os.path.join('..')))


def abrir_dataset(ruta_archivo, separador, codificacion = 'utf-8'):
    """
    Función para el Ejercicio 2.A - SOFI
    Abre el archivo principal utilizando la biblioteca estándar csv.

    """
    file = open(ruta_archivo, mode='r', encoding=codificacion)
    reader = csv.reader(file, delimiter=separador)
    header = next(reader)

    return file, reader, header

def procesar_columnas(fs: str):
    return get_columns_names(fs)


def identificar_columnas_nulas():
    file, reader, header = abrir_dataset("../raw_datasets/Occurrence.txt", ",") 

    index_null = set(range(len(header))) #creando un conjunto con los índices


    for line in reader:
        for index in list(index_null):
            if line[index].strip():
                index_null.remove(index)

        if not index_null:
            break

    file.close()
    
    columns_null = [header[index] for index in index_null]
    return columns_null 


def buscar_ruta(archivo):
    directorio = os.path.abspath(os.path.join('..', 'raw_datasets', archivo))
    return directorio