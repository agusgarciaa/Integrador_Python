import csv
import os

from collections import Counter

import src.utils.file_manager as fm
import src.utils.helpers as hp
import src.operaciones.validaciones as va
import src.operaciones.registros as re

# --------------------------------------------------------------- Ejercicios 6 - Eliminación de registros en datasets --------------------------------------------------------------
    
# Función 6.A - Sofia Martins
def eliminar_por_identificador(ruta_raw, ruta_processed, ruta_operations,identificador):
    """Elimina un registro del dataset pidiendo los valores al usuario, si existe el archivo processed trabajo sobre ese,
    sino con raw y guarda el resultado en processed usamos sniffer para imitar las caracteristicas del archivo  original y guardar en el mismo formato.
    """
    datos = []
    se_encontro = False
    eliminados = 0
    operacion = "DELETE"

    ruta_entrada = ruta_processed if os.path.exists(ruta_processed) else ruta_raw

    with open(ruta_entrada, 'r', newline='', encoding='utf-8') as archivo:
        aux = archivo.read(2048)
        aux2 = csv.Sniffer().sniff(aux)
        terminator = aux2.lineterminator
        archivo.seek(0)

        lector = csv.DictReader(archivo, dialect=aux2)
        header = lector.fieldnames

        for fila in lector:
            if fila and any(fila.values()):
                datos.append(fila)

        for fila in datos:
            if (
                fila.get('gbifID') == identificador
                or fila.get('id') == identificador
                or fila.get('occurrenceID') == identificador
            ):
                datos.remove(fila)
                se_encontro = True
                eliminados += 1
                print("se elimino el registro")
                break
            
        if not se_encontro:
            print("ese identificador no estaba en el registro")

    if se_encontro:
        fm.asegurar_directorio(ruta_processed)
        with open(ruta_processed, 'w', newline='', encoding='utf-8') as archivo_salida:
            escribir = csv.DictWriter(
                archivo_salida, fieldnames=header, lineterminator=terminator, extrasaction='ignore')
            escribir.writeheader()
            escribir.writerows(datos)

        print(f"Archivo guardado en: {ruta_processed}")
        serealizo = 'SI'
    else:
        serealizo = "ERROR"

    print(f"archivos eliminados: {eliminados}")
    re.registro_cambio_operations(ruta_operations, ruta_raw, operacion, eliminados, serealizo)


# Función 6.B - Agustin Garcia
def eliminar_registros_por_valor (ruta_raw, ruta_processed, ruta_operations, columna, valores_a_eliminar, separador =","):
    """Función que elimina registros cuyo valor en una columna pertenezca a una lista de valores suministrada por el usuario."""
    valores_a_eliminar = [v.strip() for v in valores_a_eliminar]
    operacion = "DELETE"

    try:
        with open(ruta_raw, encoding="utf-8") as archivo: 
            lector = csv.reader(archivo, delimiter=separador)
            header = next(lector)

            indice = hp.obtener_indice(header, columna)
            if indice is None:
                raise ValueError("Columna no encontrada.")

            cant_eliminados = 0

            fm.asegurar_directorio(ruta_processed)

            with open(ruta_processed, "w", newline='', encoding="utf-8") as salida: 
                escritor = csv.writer(salida, delimiter=separador)
                escritor.writerow(header)

                for fila in lector:
                    if len(fila) <= indice:
                        escritor.writerow(fila)
                        continue

                    if fila[indice] in valores_a_eliminar:
                        cant_eliminados += 1
                    else:
                        escritor.writerow(fila)

        print(f"Se eliminaron {cant_eliminados} registros.")
        re.registro_cambio_operations(ruta_operations, ruta_raw, operacion, cant_eliminados, 'SI')
        return cant_eliminados

    except Exception as e:
        print(f"Error: {e}")
        re.registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')
        return 0
    

# Ejercicio 6.C - Fe Cordoba
def eliminar_por_condicion(ruta_raw, ruta_processed, ruta_operations, columna, condicion, valor, delimiter=","):
    """Modifica el dataset procesado eliminando ciertos registros."""
    operacion = "DELETE"
    eliminados = 0

    condiciones_validas = ["==", "!=", ">", ">=", "<", "<="]
    if condicion not in condiciones_validas:
        re.registro_cambio_operations(ruta_operations, archivo, 'VALIDATION', 0, 'ERROR')
        raise ValueError("Condición no válida")

    if valor == "" or valor == "N/A":
        re.registro_cambio_operations(ruta_operations, archivo, 'VALIDATION', 0, 'ERROR')
        raise ValueError("El valor a comparar no puede ser vacío o 'N/A'")

    ruta_entrada = ruta_processed if os.path.exists(ruta_processed) else ruta_raw

    with open(ruta_entrada, newline="", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo, delimiter=delimiter)
        columnas = reader.fieldnames

        if columna not in columnas:
            re.registro_cambio_operations(ruta_operations, ruta_entrada, operacion, 0, 'ERROR')
            raise ValueError(f"La columna '{columna}' no existe")

        filas = list(reader) 

        fm.asegurar_directorio(ruta_processed)  

        with open(ruta_processed, "w", newline="", encoding="utf-8") as archivo_salida: 
            writer = csv.DictWriter(archivo_salida, fieldnames=columnas, delimiter=delimiter)
            writer.writeheader()

            for fila in filas:
                dato = fila[columna] 

                if not hp.cumple_condicion(dato, condicion, valor): 
                    writer.writerow(fila)
                else:
                    eliminados += 1 

    re.registro_cambio_operations(ruta_operations, ruta_entrada, operacion, eliminados, 'SI')


# Función 6.E - Ana Freitas y 6.F - Lucía Cipolla
def sanitizar_dataset(ruta_raw, ruta_processed, ruta_operations, separador=','):
    """Sanitización automática de datasets. Recibe la ruta del archivo original y la ruta de destino en processed_datasets."""
    registros_sanitizados = []
    motivo_eliminacion = Counter()
    indices = set()
    operacion = "DELETE"
    eliminados = 0
    total_registros = 0
    codigos_validos = ['AR', 'BO', 'BR', 'PY', 'UY', 'CH']

    ruta_entrada = ruta_processed if os.path.exists(ruta_processed) else ruta_raw

    try:
        with open(ruta_entrada, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo, delimiter=separador)
            header = lector.fieldnames

            for fila in lector:
                es_valido,motivo = va.es_registro_valido(fila, indices, codigos_validos)
                if es_valido:
                    registros_sanitizados.append(fila)
                else:
                    motivo_eliminacion[motivo] += 1
                    eliminados += 1
                total_registros += 1

        fm.asegurar_directorio(ruta_processed) 
        
        with open(ruta_processed, mode='w', encoding='utf-8', newline='') as archivo_salida:
            escritor = csv.DictWriter(archivo_salida, fieldnames=header, delimiter=separador)
            escritor.writeheader()
            escritor.writerows(registros_sanitizados)
            
        print(f"Sanitización finalizada. Registros conservados: {len(registros_sanitizados)}")
        print(f"Registros eliminados: {eliminados}")

        if total_registros > 0:
            print(f"Porcentaje de registros eliminados: {eliminados/total_registros:.2%}")

        for motivo,cantidad in motivo_eliminacion.items():
            print(f"Motivo de eliminación: {motivo} - {cantidad}")

        re.registro_cambio_operations(ruta_operations, ruta_raw, operacion, eliminados, 'SI')

    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo en {ruta_entrada}")
        re.registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        re.registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')




