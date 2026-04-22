import csv
import sys
import os
from src.file_manager import abrir_dataset; 

from pathlib import Path


# Funciones para encontrar las rutas de los archivos --- Ana Freitas
def _obtener_raiz_proyecto():
    """
    Encuentra la carpeta principal del proyecto.
    Usa la ubicación de este archivo como referencia para subir niveles 
    hasta la raíz, garantizando que funcione en cualquier computadora.
    """
    return Path(__file__).parent.parent.absolute()

def obtener_ruta_de_datos(filename):
    """
    Construye la ruta final hacia un archivo específico en 'raw_datasets'.
    Recibe el nombre del archivo y devuelve la dirección completa como texto.
    """
    # Primero localizamos dónde empieza nuestro proyecto
    root = _obtener_raiz_proyecto()
    
    # Unimos la raíz con la carpeta de datos y el nombre del archivo
    ruta_completa = root / 'raw_datasets' / filename
    
    # Lo convertimos a string para que sea fácil de usar en pandas o funciones de os
    return str(ruta_completa)



# Ejercicio 2.D - Agustin Garcia
def total_registros (ruta, separador=",", encoding="utf-8"):
    """
    Abre un dataset en formato CSV y cuenta la cantidad de registros, retornando el total. 
    """
    total = 0

    with open(ruta, newline='', encoding=encoding) as archivo_dataset:
        lector = csv.reader(archivo_dataset, delimiter=separador)
        next(lector)
        
        for _ in lector:
            total += 1

    return total



# Ejercicio 2.E - Fe Cordoba 
def columnas_con_nulos(ruta, separador=","):
    columnas_con_null = set() 

    with open(ruta, encoding="utf-8") as archivo:  
        lector = csv.reader(archivo, delimiter=separador)
        
        header = next(lector) 

        for fila in lector:
            for i, valor in enumerate(fila):
                if valor.strip() == "" or valor.strip() == "N/A":
                    columnas_con_null.add(header[i])

    return list(columnas_con_null)



# Ejercicio 2.F - Fe Cordoba 
def porcentaje_nulos(ruta, separador=","):
    with open(ruta, encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        
        header = next(lector)
        cantidad_columnas = len(header)

        nulos = [0] * cantidad_columnas
        total_filas = 0

        for fila in lector:
            total_filas += 1
            for i, valor in enumerate(fila):
                if valor.strip() == "" or valor.strip() == "N/A":
                    nulos[i] += 1

    porcentajes = {}

    for i in range(cantidad_columnas):
        if total_filas > 0:
            porcentajes[header[i]] = (nulos[i] / total_filas) * 100
        else:
            porcentajes[header[i]] = 0

    return porcentajes



# Ejercicio 2.G - Agustin Garcia
def contar_valores_distintos (nombre_columna, ruta, separador=",", encoding="utf-8"):
    valores = []

    with open(ruta, newline='', encoding=encoding) as archivo_dataset:
        lector = csv.reader(archivo_dataset, delimiter=separador)
        header = [columna.strip() for columna in next(lector)]   # Lee la primer fila

        if nombre_columna not in header:
            print("No se encontró la columna específicada. ")
            return None
        else:
            i = header.index(nombre_columna)   # Indice para tomar la columna de manera directa
        
            for registro in lector:
                if registro[i] not in valores:   # Si el valor no fue usado por otro registro se agrega a la lista
                    valores.append(registro[i])
        
    return len(valores)   # Retorna el total de valores distintos



# Ejercicio 2.J - Ana Freitas
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
















# Ejercicio 3.C - Fe Cordoba
from datetime import datetime  #  Es una clase que sirve para trabajar con fechas y horas

    #  Funcion auxiliar 

def chequear_fecha(valor):
    # intenta convertir el string a fecha usando varios formatos

    formatos = ["%d-%m-%Y","%Y-%m-%d", "%m-%Y", "%Y", "%Y-%m-%dT%H:%M:%S"]

    for formato in formatos:
        try:
            # si el formato coincide, devuelve la fecha
            return datetime.strptime(valor, formato)  #  aca convierte el str a fecha (si puede)
        except:
            # si falla, prueba con el siguiente formato
            pass

    # si ninguno funciona, no es una fecha válida
    return None

    #  Funcion principal 

def validar_fechas(ruta, separador=","):
    fechas_invalidas = {}  # {fila: [(columna, valor, motivo)]}

    with open(ruta, encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        header = next(lector)

        columnas_fecha = ['eventdate', 'verbatimeventdate']

        indices_fecha = []
        for i, col in enumerate(header):
            if col.strip().lower() in columnas_fecha:
                indices_fecha.append(i)

        print("Columnas detectadas como fecha:")
        print([header[i] for i in indices_fecha])

        # recorre cada fila del dataset
        for num_fila, fila in enumerate(lector, start=1):
            for i in indices_fecha:

                # evita error si la fila tiene menos columnas
                valor = fila[i].strip() if i < len(fila) else ""

                # ignora valores nulos
                if valor == "" or valor.lower() == "n/a":
                    continue

                fecha = chequear_fecha(valor)

                # guarda error si no se puede convertir
                if fecha is None:
                    fechas_invalidas.setdefault(num_fila, []).append(
                        (header[i], valor, "formato inválido")
                    )

                # guarda error si la fecha es futura
                elif fecha > datetime.now():
                    fechas_invalidas.setdefault(num_fila, []).append(
                        (header[i], valor, "fecha futura")
                    )

    return fechas_invalidas















# Ejercicio 3.E - Fe Cordoba
def validar_country_code(ruta, separador=","):
    cods_invalidos = {}  # {fila: [(columna, valor, motivo)]}
    codigos_validos = ['AR','BO','BR','PY','UY','CH']

    with open(ruta, encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        header = next(lector)

        # verifica si la columna existe para evitar errores
        if "countryCode" not in header:
            return {"error": "No existe la columna countryCode"}

        # obtiene la posición de la columna en el header
        indice = header.index("countryCode")

        # recorre cada fila
        for num_fila, fila in enumerate(lector, start=1):

            # evita error si faltan columnas
            valor = fila[indice].strip() if indice < len(fila) else ""

            # detecta valores nulos
            if valor == "" or valor.lower() == "n/a":
                cods_invalidos.setdefault(num_fila, []).append(
                    ("countryCode", valor, "nulo")
                )

            # detecta códigos distintos de codigos validos
            
            elif valor not in  codigos_validos:
                cods_invalidos.setdefault(num_fila, []).append(
                    ("countryCode", valor, "código inválido")
                )

    return cods_invalidos









