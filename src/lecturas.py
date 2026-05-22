import csv

from collections import Counter

import src.helpers as hp


# --------------------------------------------------------------- Ejercicios 2 - Lectura del dataset --------------------------------------------------------------
   
#funcion 2a sofia martins
def recorrer_diez_filas(ruta,delimiterr):
    """abre un dataset y imprime las primeras 10 filas"""
    with open(ruta, mode='r', encoding='utf-8') as archivo:
        next(archivo)
        modo = csv.reader(archivo, delimiter=delimiterr)
        for i, fila in enumerate(modo):
            if i < 10:
                print(fila)
            else:
                break


#funcion 2b sofia martins
def imprimir_encabezados(ruta, delimiter=','):
    """retorna el encabezado del dataset"""
    archivo = open(ruta, 'r', encoding='utf-8')
    modo = csv.reader(archivo, delimiter=delimiter)
    encabezado=next(modo)
    archivo.close()
    return encabezado


# Ejercicio 2.C - Lucia Cipolla
def column_index (path,c_delimiter=',',c_encoding='utf-8'):
    """
        Recibe el path de un archivo en formato csv y lo lee.
        Devuelve un diccionario que tiene como clave el nombre de la columna y como valor el indice(desde 0).
        Parametros:
            path: un path (mejor si es un r-string)
            c_delimeter: por defecto seteado en ',' indica el delimeter al leer el archivo con csv.reader()
            c_encoding: por defecto seteado en 'utf-8' indica el encoding al abrir el archivo con open()

        se usan las librerias: csv
    """
    dict_index = {}
    try:
        with open(path, mode='r', encoding=c_encoding) as archivo:
            lector = csv.reader(archivo, delimiter=c_delimiter)
            header = next(lector)
            for i, columna in enumerate(header):
                dict_index[columna] = i
    except FileNotFoundError:
        print('No se encontró el archivo. ')
    return dict_index


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
def contar_valores_distintos(nombre_columna, ruta, separador=",", encoding="utf-8"):
    valores = set() # Colección de elementos únicos.

    with open(ruta, newline='', encoding=encoding) as archivo_dataset:
        lector = csv.reader(archivo_dataset, delimiter=separador)
        header = [columna.strip() for columna in next(lector)]

        if nombre_columna not in header:
            print("No se encontró la columna especificada.")
            return None
        
        i = header.index(nombre_columna)

        for registro in lector:
            if len(registro) > i:
                valores.add(registro[i])  # Si ya existe, no agrega.

    return len(valores)


# Ejercicio 2.H - Lucia Cipolla
def frecuencia_de_valores (path,nombre,c_delimiter=',',c_encoding='utf-8'):
    """
        Recibe el path de un archivo en formato csv y lo lee.
        Recibe en nombre el nombre o posición de una columna.
        Devuelve un diccionario que tiene como clave el nombre del valor de la columna y como valor la
        cantidad de veces que aparece repetido.
        Parametros:
            path: un path (mejor si es un r-string)
            c_delimeter: por defecto seteado en ',' indica el delimeter al leer el archivo con csv.reader()
            c_encoding: por defecto seteado en 'utf-8' indica el encoding al abrir el archivo con open()
            nombre: nombre o índice de la columna a analizar.

        se usan las librerias: csv, collections(Counter)
    """
    freq = Counter()
    nombre = str(nombre)
    try:
        with open(path, mode='r', encoding=c_encoding) as archivo:
            lector = csv.reader(archivo, delimiter=c_delimiter)
            header = next(lector)
            match nombre.isdigit():
                case True:
                    nombre = int(nombre)
                    if (nombre <= len(header)):
                        for elemento in lector:
                            freq[elemento[nombre]]+= 1
                    else:
                        print(f'El número ingresado excede la cantidad de columnas. La columna {nombre} no existe. ')
                case False:
                    if nombre in header:
                        pos = header.index(nombre)
                        for elemento in lector:
                            freq[elemento[pos]]+= 1
                    else:
                        print('No se encontró la columna.')
    except FileNotFoundError:
        print('No se encontró el archivo. ')

    freq=dict(freq)
    return freq


# Ejercicio 2.I - Ana Freitas 
def verificar_tipo(ruta, separador, columna, tipo_dato):
    """
    Coordina la lectura del archivo fila por fila (eficiente en memoria)
    y delega el cálculo de métricas según el tipo de dato (numérico, texto o coordenadas).
    """
    try:
        with open(ruta, mode='r', encoding="utf-8") as archivo:
            lector = csv.reader(archivo, delimiter=separador)
            header = next(lector)
            
            indice = hp.obtener_indice(header, columna)
            if indice is None or indice == -1:
                print(f"Error: No se encontró la columna '{columna}' en el dataset.")
                return None

            if tipo_dato == 'numeric':
                return hp.calcular_numericos(lector, indice)
            elif tipo_dato == 'text':
                return hp.calcular_text(lector, indice)
            elif tipo_dato == 'coordinate':
                return hp.calcular_coordenada(lector, indice)
            else:
                print(f"Error: El tipo de dato '{tipo_dato}' no es válido.")
                return None

    except FileNotFoundError:
        print(f"Error Crítico: No se pudo encontrar el archivo en la ruta: {ruta}")
        return None
    except PermissionError:
        print(f"Error de Permisos: No se puede leer el archivo en {ruta}.")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado al procesar el dataset: {e}")
        return None
    

# Ejercicio 2.J - Ana Freitas
def identificar_columnas_nulas(ruta, separador):
    """
    Identifica qué columnas del dataset no tienen ningún dato cargado 
    en ninguno de los registros (están 100% vacías).
    Devuelve una lista con los nombres de las columnas vacías.
    """
    try:
        with open(ruta, mode='r', encoding="utf-8") as archivo:
            lector = csv.reader(archivo, delimiter=separador)
            header = next(lector)

            indices_vacios = set(range(len(header)))

            for line in lector:
                for index in list(indices_vacios):
                    if index < len(line):
                        valor = line[index].strip()
                        if valor and valor.upper() != "N/A":
                            indices_vacios.remove(index)

                if not indices_vacios:
                    break
        
        columnas_vacias = [header[index] for index in indices_vacios]
        
        return columnas_vacias

    except FileNotFoundError:
        print(f"Error Crítico: No se pudo encontrar el archivo en la ruta: {ruta}")
        return []
    except PermissionError:
        print(f"Error de Permisos: No se puede leer el archivo en {ruta}.")
        return []
    except Exception as e:
        print(f"Ocurrió un error inesperado al procesar el dataset: {e}")
        return []