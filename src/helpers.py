from collections import Counter
from datetime import datetime
import csv
import os

# ----------------------------------------- Funciones de apoyo - sirven de base para los ejercicios del proyecto. -----------------------------------------

# Function para obtener el indice de una columna - Ana Freitas
def obtener_indice(header, columna):
    header_limpio = [col.strip().lower() for col in header] # Limpia espacios invisibles en el header
    nombre_columna = columna.strip().lower() 
    
    try:
        return header_limpio.index(nombre_columna)
    except ValueError:
        print(f" Error: No se encontró la columna: {columna}")
        return None
    

# Funcion de apoyo para el ejercicio 2.I - Ana Freitas
def calcular_numericos(lista):
    numeros = [float(num) for num in lista if num.strip()] # Crea una lista de números sin los espacios en blanco

    return 'menor valor encontrado: ', min(numeros), 'mayor valor encontrado: ',  sum(numeros), 'promedio: ', sum(numeros) / len(lista)


# Funcion de apoyo para el ejercicio 2.I - Ana Freitas
def calcular_text(lista):
    texto = [len(text.strip()) for text in lista] # Crea una lista de strings sin los espacios en blanco 

    return min(texto), max(texto)


# Funcion de apoyo para el ejercicio 2.I - Ana Freitas
def calcular_coordenada(lista):
    coordenada = [float(num) for num in lista]

    return max(coordenada), min(coordenada)


# Funcion de apoyo para el ejercicio 3.A - Sofia Martins
def numero(dato):
    aux=dato.strip().replace('-','',1).replace('.','',1)
    return aux.isdigit()and dato.strip() !=""


# Funcion de apoyo para el ejercicio 3.D - Ana Freitas
def detectar_duplicados(lista):
    conteo_ids = Counter(lista) 
    
    repetidos = [id for id, cantidad in conteo_ids.items() if cantidad > 1]
    duplicados = sum(cantidad - 1 for cantidad in conteo_ids.values() if cantidad > 1)
    
    return 'registros duplicados: ', duplicados, 'identificador se repite: ', repetidos


# Funcion para el ejercicio 3.C - Fe Cordoba
def chequear_fecha(valor):
    """
    Intenta convertir un string a fecha usando distintos formatos.
    Retorna un objeto datetime si es válido, o None si no lo es.
    """

    formatos = [
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%m-%Y",
        "%Y",
        "%Y-%m-%dT%H:%M:%S"
    ]

    for formato in formatos:
        try:
            return datetime.strptime(valor, formato)
        except ValueError:
            continue

    return None


# Funcion de apoyo para el ejercicio 3.G - Agustin Garcia
def contar_taxonomia_incompleta(ruta, separador=","):
    incompletos = 0
    informacion_taxonomica_valida = ["kingdom", "phylum", "class", "order", "family", "genus", "specificEpithet", "scientificName"]

    with open(ruta, encoding="utf-8") as dataset:
        reader = csv.DictReader(dataset, delimiter=separador)

        columnas_presentes = reader.fieldnames
        columnas_a_revisar = []
        
        for col in informacion_taxonomica_valida:
            if col in columnas_presentes:
                columnas_a_revisar.append(col)

        for fila in reader:
            es_incompleto = False
            
            for col in columnas_a_revisar:
                valor = fila.get(col, "")
                
                if valor == "":
                    es_incompleto = True
                    break # Si la columna devuelve un incompleto, se deja de revisar.
            
            if es_incompleto == True:
                incompletos = incompletos + 1

    return incompletos


# Función para obtener el último id de un dataset. 
def obtener_ultimo_id(ruta, separador, columna_id, es_xeno=False):
    ultimo_id = 0

    with open(ruta, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo, delimiter=separador)

        for fila in lector:
            valor = fila.get(columna_id)

            if not valor:
                continue

            if es_xeno:
                if "@XC" in valor:
                    valor = valor.split("@")[0]
                else:
                    continue

            if valor.isdigit():
                ultimo_id = max(ultimo_id, int(valor))

    return ultimo_id


# Helper para la funcion cumple condicion - Fe Cordoba
def es_numero(valor):
    """Determina si un valor es numérico (incluye negativos y decimales)."""

    if valor == "" or valor == "N/A":
        return False

    valor_str = str(valor)

    if valor_str.startswith("-"):
        valor_str = valor_str[1:]

    valor_str = valor_str.replace(".", "", 1)

    return valor_str.isdigit()


# Helper para la funcion del 6.C - Fe Cordoba
def cumple_condicion(dato, condicion, valor):
    """Evalúa si un dato cumple una condición."""

    if dato == "" or dato == "N/A":
        return False

    if es_numero(dato) and es_numero(valor):
        dato = float(dato)
        valor = float(valor)
    else:
        dato = str(dato)
        valor = str(valor)

    match condicion:
        case "==":
            return dato == valor
        case "!=":
            return dato != valor
        case ">":
            return dato > valor
        case ">=":
            return dato >= valor
        case "<":
            return dato < valor
        case "<=":
            return dato <= valor
        case _:
            # esto no debería ocurrir si validamos antes
            raise ValueError("Condición no válida")


#Función de apoyo para la función 3.H - Lucía Cipolla
def check_coordenadas (dato, MAX, MIN):
    try:
        dato = float(dato)
        if dato<MIN or dato>MAX:
            res=False
        else:
            res=True
    except ValueError:
        res=False

    return res


#Función de apoyo para la función 3.A - Sofia Martins
def verificar_latitud(latitud):
    cumple=True
    if not numero(latitud) or not(-90<=float(latitud)<=90):
        cumple=False
    return cumple


def verificar_longitud(longitud):
    cumple=True
    if not numero(longitud) or not(-180<=float(longitud)<=180):
        cumple=False
    return cumple


# funcion de apoyo para las que crean/modifican processed datasets
def asegurar_directorio(ruta_archivo):
    carpeta = os.path.dirname(ruta_archivo)
    os.makedirs(carpeta, exist_ok=True)