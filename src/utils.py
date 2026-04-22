import csv


def abrir_dataset(ruta_archivo, separador, codificacion):
    """
    Función para el Ejercicio 2.A - SOFI
    Abre el archivo principal utilizando la biblioteca estándar csv.

    """
    print("hello world") 


<<<<<<< HEAD
def total_records (route, sep=",", encoding="utf-8"):
    """
    Abre un dataset en formato CSV y cuenta la cantidad de registros, retornando el total. Ejercicio 2.D.
    """
    total = 0

    with open(route, newline='', encoding=encoding) as dataset_file:
        reader = csv.reader(dataset_file, delimiter=sep)

        for _ in reader:
            total += 1

    return total


def count_distinct_values(column_name, route, sep=",", encoding="utf-8"):
    values = []

    with open(route, newline='', encoding=encoding) as dataset_file:
        reader = csv.reader(dataset_file, delimiter=sep)
        header = [column.strip() for column in next(reader)]   # Lee la primer fila

        if column_name not in header:
            print("No se encontró la columna específicada. ")
            return None
        else:
            i = header.index(column_name)   # Indice para tomar la columna de manera directa
        
            for record in reader:
                if record[i] not in values:   # Si el valor no fue usado por otro registro se agrega a la lista
                    values.append(record[i])
        
    return len(values)   # Retorna el total de valores distintos
=======






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









>>>>>>> upstream/main
