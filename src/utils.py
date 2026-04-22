import csv


def abrir_dataset(ruta_archivo, separador, codificacion):
    """
    Función para el Ejercicio 2.A - SOFI
    Abre el archivo principal utilizando la biblioteca estándar csv.

    """
    print("hello world") 


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
