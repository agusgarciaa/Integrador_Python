from collections import Counter
from datetime import datetime

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