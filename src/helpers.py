from collections import Counter
from datetime import datetime
from pathlib import Path
import csv
import src.validaciones as va

# ----------------------------------------- Constantes de apoyo - sirven de base para los ejercicios del proyecto. -----------------------------------------

MAX_LAT = 13.0
MIN_LAT = -56.0
MAX_LONG = -34.0
MIN_LONG = -82.0

COUNTRY_CODES = ['AR', 'BO', 'BR', 'PY', 'UY', 'CL']

# ----------------------------------------- Funciones de apoyo - sirven de base para los ejercicios del proyecto. -----------------------------------------

# Function para obtener el indice de una columna - Ana Freitas
def obtener_indice(header, columna):
    """
    Busca la posición numérica de una columna en el encabezado,
    normalizando el texto para evitar errores por mayúsculas o espacios.
    """
    header_limpio = [col.strip().lower() for col in header]
    nombre_columna = columna.strip().lower() 
    
    try:
        return header_limpio.index(nombre_columna)
    except ValueError:
        print(f" Error: No se encontró la columna: {columna}")
        return None
    

# Funcion de apoyo para el ejercicio 2.I - Ana Freitas
def calcular_numericos(lista):
    """
    Calcula el mínimo, máximo y promedio de una lista de valores numéricos.
    """
    numeros = [float(num) for num in lista if num.strip()] 

    menor = min(numeros)
    mayor = max(numeros)
    promedio = sum(numeros) / len(numeros) if numeros else 0

    return 'menor valor encontrado: ', menor, 'mayor valor encontrado: ', mayor, 'promedio: ', promedio


# Funcion de apoyo para el ejercicio 2.I - Ana Freitas
def calcular_text(lista):
    """
    Analiza la longitud de las cadenas de texto en la columna.
    """
    texto = [len(text.strip()) for text in lista] 
    
    return min(texto), max(texto)


# Funcion de apoyo para el ejercicio 2.I - Ana Freitas
def calcular_coordenada(lista):
    """
    Calcula los extremos geográficos (mínimo y máximo) de una lista de coordenadas.
    """
    coordenada = [float(num) for num in lista if num.strip()]

    return max(coordenada), min(coordenada)


# Funcion de apoyo para el ejercicio 3.A - Sofia Martins
def numero(dato):
    aux=dato.strip().replace('-','',1).replace('.','',1)
    return aux.isdigit()and dato.strip() !=""


# Funcion de apoyo para el ejercicio 3.D - Ana Freitas
def detectar_duplicados(lista):
    """
    Analiza una lista de identificadores y reporta la cantidad y cuáles son los duplicados.
    """
    conteo_ids = Counter(lista) 
    
    repetidos = [id for id, cantidad in conteo_ids.items() if cantidad > 1]
    duplicados = sum(cantidad - 1 for cantidad in conteo_ids.values() if cantidad > 1)
    
    return 'registros duplicados: ', duplicados, 'identificador se repite: ', repetidos


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


# Helper para 1.b de la segunda parte.
def obtener_nombres_datasets():

    ruta_datasets = Path("processed_datasets")

    datasets = []

    for carpeta in ruta_datasets.iterdir():

        if carpeta.is_dir():
            datasets.append(carpeta.name)

    return datasets


# para 2.b Fe Cordoba
# obtener valores de una columna 
def obtener_opciones(df, columna):
    """Obtiene los valores únicos, no nulos y como texto de una columna."""
    valores = df[columna]
    return sorted(
        valores
        .dropna()
        .astype(str)
        .unique()
    )


# obtiene los country code del dataframe
def obtener_paises_validos(df):
    """Filtra y obtiene los country codes válidos del dataframe."""
    codigos = (
        df["countryCode"]
        .dropna()
        .astype(str)
        .unique()
    )

    codigos_validos = []
    for codigo in codigos:
        if not va.validar_country_code_registro(codigo, COUNTRY_CODES):
            codigos_validos.append(codigo)

    return sorted(codigos_validos)


# Helpers para la función 2.C
def obtener_columnas_relevantes(nombre_dataset, columnas_disponibles, columnas_relevantes_constante):
    relevantes = columnas_relevantes_constante.get(nombre_dataset, [])
    if not relevantes:
        return None
    return [columna for columna in relevantes if columna in columnas_disponibles]

def paginar(df, pagina, registros_por_pagina):
    total = len(df)
    total_paginas = max(1, (total + registros_por_pagina - 1) // registros_por_pagina)
    pagina = max(1, min(pagina, total_paginas))
    inicio = (pagina - 1) * registros_por_pagina
    fin = min(inicio + registros_por_pagina, total)
    return df.iloc[inicio:fin], inicio, fin, total_paginas
