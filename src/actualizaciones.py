import csv
import os

import src.file_manager as fm
import src.helpers as hp
import src.validaciones as va
import src.registros as re
import src.lecturas as le

# --------------------------------------------------------------- Ejercicios 5 - Actualización de registros en datasets --------------------------------------------------------------

# Ejercicio 5.A - Lucía Cipolla
def registrar_filtro (path,c_delimiter=',',c_encoding='utf-8',**kwargs):
    """
        Recibe el path de un archivo en formato csv y lo lee.
        Devuelve una lista de listas con las filas que pasan el filtro. Se filtra con una lógica AND. Si un parámetro es inválido se ignora.
        Si ninguna fila cumple se devuelve el diccionario vacío.
        Parametros:
            path: un path (mejor si es un r-string)
            c_delimeter: por defecto seteado en ',' indica el delimeter al leer el archivo con csv.reader()
            c_encoding: por defecto seteado en 'utf-8' indica el encoding al abrir el archivo con open()
            **kwargs: un diccionario con una cantidad indeterminada de parámetros.
            
        se usan las librerias: csv
    """
    col_index = le.column_index(path,c_delimiter,c_encoding)

    i=[]
    val=[]
    for col in kwargs:
        try:
            i.append(col_index[col])
            val.append(str(kwargs[col]).strip().lower())
        except KeyError:
            print(f'La columna {col} no existe')

    if len(kwargs)>0 and len(i)==0:
        print('No se encontraron columnas válidas.')
        return []

    with open(path,mode='r',encoding=c_encoding) as archivo:
        lector = csv.reader(archivo,delimiter=c_delimiter)
        header = next(lector)

        ret = []

        for fila in lector:  
            valido = True
            for n,columna in enumerate(i):  
                cel = fila[columna]  
                if (str(cel).strip().lower() != val[n]):
                    valido = False
                    break
            if (valido==True):
                ret.append(fila)

    return ret


# Ejercicio 5.B - Ana Freitas
def actualizar_campo(ruta_raw, ruta_processed, ruta_operations, separador, identificador, columna, nuevo_valor):
    """
    Actualiza un valor validando consistencia y reportando errores.
    """
    operacion = "UPDATE"
    afectados = 0
 
    ruta_entrada = ruta_processed if os.path.exists(ruta_processed) else ruta_raw
    
    dict_val = {columna: nuevo_valor}
    resultados_val = va.validar(**dict_val)
    es_valido = resultados_val.get(columna, True) 

    if not es_valido:
        print(f"Error: El valor '{nuevo_valor}' no es válido para la columna '{columna}'.")
        re.registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')
        return

    registros_actualizados = []

    try:
        with open(ruta_entrada, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo, delimiter=separador)
            columnas = lector.fieldnames

            if columna not in columnas:
                print(f"Error: La columna '{columna}' no existe en el dataset.")
                return

            for fila in lector:
                id_en_archivo = str(fila.get("id", "").strip() or fila.get("gbifID", "").strip() or fila.get("occurrenceID", "").strip())
                id_buscado = str(identificador).strip()
        
                if id_en_archivo == id_buscado:
                    fila[columna] = str(nuevo_valor)
                    afectados += 1
                
                registros_actualizados.append(fila)

        if afectados > 0:
            fm.asegurar_directorio(ruta_processed)
            with open(ruta_processed, mode='w', encoding='utf-8', newline='') as archivo_salida:
                escritor = csv.DictWriter(archivo_salida, delimiter=separador, fieldnames=columnas)
                escritor.writeheader()
                escritor.writerows(registros_actualizados)
            
            print(f"Éxito: Se actualizaron {afectados} registro(s).")
            re.registro_cambio_operations(ruta_operations, ruta_raw, operacion, afectados, 'SI')
        else:
            print(f"Error: No se realizaron cambios. No existe el id: '{identificador}'")
            re.registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')

    except Exception as e:
        print(f"Error inesperado: {e}")
        re.registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')


# Ejercicio 5.C - Ana Freitas
def actualizar_multiples_campos(ruta_raw, ruta_processed, ruta_operations, separador, identificador, dic_cambios):
    """
    Actualiza múltiples campos de un registro específico en una sola operación.
    """
    operacion = "UPDATE"
    afectados = 0

    ruta_entrada = ruta_processed if os.path.exists(ruta_processed) else ruta_raw

    resultados_val = va.validar(**dic_cambios)
    campos_invalidos = [col for col, valido in resultados_val.items() if not valido]
    
    if campos_invalidos:
        for col in campos_invalidos:
            print(f"Error: El valor para la columna '{col}' es inválido.")
        re.registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')
        return

    registros_para_guardar = []

    try:
        with open(ruta_entrada, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo, delimiter=separador)
            columnas = lector.fieldnames

            columnas_invalidas = [col for col in dic_cambios if col not in columnas]
            if columnas_invalidas:
                print(f"Error: Las columnas {columnas_invalidas} no existen en este dataset.")
                return
            
            for fila in lector:
                id_en_archivo = str(fila.get("id", "").strip() or  fila.get("gbifID", "").strip() or  fila.get("occurrenceID", "").strip())
                id_buscado = str(identificador).strip()

                if id_en_archivo == id_buscado:
                    fila.update({k: str(v) for k, v in dic_cambios.items()})
                    afectados += 1
                
                registros_para_guardar.append(fila)

        if afectados > 0:
            fm.asegurar_directorio(ruta_processed)
            with open(ruta_processed, mode='w', encoding='utf-8', newline='') as archivo_salida:
                escritor = csv.DictWriter(archivo_salida, delimiter=separador, fieldnames=columnas)
                escritor.writeheader()
                escritor.writerows(registros_para_guardar)
            
            print(f"Éxito: Se actualizaron {afectados} registro(s) con múltiples campos.")
            re.registro_cambio_operations(ruta_operations, ruta_raw, operacion, afectados, 'SI')
        else:
            print(f"Error: No se encontró el registro con ID '{identificador}'")
            re.registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')

    except Exception as e:
        print(f"Ocurrió un error inesperado al actualizar: {e}")
        re.registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')
