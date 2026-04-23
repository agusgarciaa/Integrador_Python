import csv;


def abrir_dataset(ruta_archivo, separador, codificacion = 'utf-8'):
    """
    Función para el Ejercicio 2.A - SOFI
    Abre el archivo principal utilizando la biblioteca estándar csv.

    """
    file = open(ruta_archivo, mode='r', encoding=codificacion)
    reader = csv.reader(file, delimiter=separador)
    header = next(reader)

    return file, reader, header

