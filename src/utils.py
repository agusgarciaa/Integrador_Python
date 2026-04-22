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
<<<<<<< HEAD
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
=======
    print("hello world") 








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









>>>>>>> a4914e8eb82471d67ce1a207f0d62bb51263d584
