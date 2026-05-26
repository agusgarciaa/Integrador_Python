import csv
import os

import src.file_manager as fm
import src.helpers as hp
import src.validaciones as va
import src.registros as re

# --------------------------------------------------------------- Ejercicios 4 - Inserción de registros en datasets --------------------------------------------------------------

#  Ejercicio 4.A/B - Fe Cordoba
def crear_registro_vacio(columnas):
    columnas_id = ["id", "occurrenceid", "gbifid"]
    
    registro = {}   # crea el registro con none en sus columnas ignorando posibles ids 
    for col in columnas:
        if col.strip().lower() not in columnas_id:  
            registro[col] = None

    return registro


# Ejercicio 4.C - Agustin Garcia
def validar_registro(registro, separador=','):
    errores = []
    es_valido = True
    codigos_validos = ['AR','BO','BR','PY','UY','CH']
    campos_tax = ["kingdom", "phylum", "class", "order", "family", "genus", "specificEpithet", "scientificName"]

    # Validación de coordenadas
    lat = registro.get("decimalLatitude")
    lon = registro.get("decimalLongitude")

    if not hp.numero(lat) or not hp.numero(lon):
        errores.append("Coordenadas inválidas")
    else:
        lat = float(lat)
        lon = float(lon)
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            errores.append("Coordenadas fuera de rango")

    # Validación de fecha
    fecha = registro.get("eventDate")
    if fecha:
        fecha_a_verificar = va.chequear_fecha(fecha)
        if fecha_a_verificar is None:
            errores.append("Fecha inválida")

    # Validación de CountryCode
    country = registro.get("countryCode")
    if country and country not in codigos_validos:
        errores.append("CountryCode inválido")

    # Validación de taxonomía
    for campo in campos_tax:
        if campo in registro and registro[campo] == "":
            errores.append(f"Falta {campo}")

    if len(errores) != 0:
        es_valido = False
    return errores, es_valido
    

# Función 4.D - Agustin Garcia
def preparar_registro(registro, dataset, ruta, separador=","):
    """
    Recibe un registro sin ID y devuelve uno listo para insertar,
    agregando el ID correspondiente.
    """
    registro_final = registro.copy()

    if dataset == "iadiza":
        col_id = "gbifID"
        ultimo_id = hp.obtener_ultimo_id(ruta, separador, col_id)

    elif dataset == "xenocanto":
        col_id = "id"
        ultimo_id = hp.obtener_ultimo_id(ruta, separador, col_id, es_xeno=True)

    elif dataset == "inaturalist":
        col_id = "id"
        ultimo_id = hp.obtener_ultimo_id(ruta, separador, col_id)

    else:
        raise ValueError("Dataset desconocido")

    # generar ID
    if dataset == "xenocanto":
        nuevo_id = f"{ultimo_id + 1}@XC"
    else:
        nuevo_id = str(ultimo_id + 1)

    registro_final[col_id] = nuevo_id

    return registro_final


# Funcion 4.F - Sofia Martins
def agregar_registro(ruta_raw, ruta_processed, ruta_operations):
    """
    Agrega un registro al dataset pidiendo los valores al usuario,
    si existe el archivo processed trabajo  sobre ese,sino con raw y guarda el resultado en processed
    usamos sniffer para imitar las caracteristicas del archivo original y guardar en el mismo formato.
    """
    datos = []
    agregados=0
     
    ruta_entrada = ruta_processed if os.path.exists(ruta_processed) else ruta_raw

    with open(ruta_entrada, 'r', newline='', encoding='utf-8') as archivo:
        muestra = archivo.read(2048)
        codificacion = csv.Sniffer().sniff(muestra)
        terminator = codificacion.lineterminator
        archivo.seek(0)
        lector = csv.DictReader(archivo, dialect=codificacion)
        header = lector.fieldnames
        for fila in lector:
            if fila and any(fila.values()):
                datos.append(fila)
    nuevo=crear_registro_vacio(header)
    for columna in nuevo.keys():
        valor = input(f'Ingrese el valor en la columna [{columna}]: ') 
        nuevo[columna] = valor
    final={}
    for columna in header:
        if columna in nuevo:
            final[columna]=nuevo[columna]
        else:
            final[columna]=input("ingrese un id: ")     
    datos.append(final)
    agregados +=1
    
    fm.asegurar_directorio(ruta_processed)
    with open(ruta_processed, 'w', newline='', encoding='utf-8') as archivo_salida:
        escribir = csv.DictWriter(archivo_salida, fieldnames=header, lineterminator=terminator,extrasaction='ignore')
        if not os.path.isfile(ruta_processed) and os.path.getsize(ruta_processed) == 0:
           escribir.writeheader()
        escribir.writerows(datos)
    
    print(f"Archivo guardado en: {ruta_processed}")
    operacion="INSERT"
    serealizo="SI"
    re.registro_cambio_operations(ruta_operations,ruta_raw,operacion,agregados,serealizo)


# Funcion 4.G - Sofia Martins
def agregar_varios_registros(ruta_raw,ruta_processed,ruta_operations):  
    """
    Agregan varios registros al dataset pidiendo los valores al usuario,
    si existe el archivo processed trabajo  sobre ese,sino con raw y guarda el resultado en processed
    usamos sniffer para imitar las caracteristicas del archivo original y guardar en el mismo formato.
    """
    datos = []
    agregados=0
    
    ruta_entrada = ruta_processed if os.path.exists(ruta_processed) else ruta_raw
     
    with open(ruta_entrada, 'r', newline='', encoding='utf-8') as archivo:
        muestra = archivo.read(2048)
        codificacion = csv.Sniffer().sniff(muestra)
        terminator = codificacion.lineterminator
        archivo.seek(0)
        lector = csv.DictReader(archivo, dialect=codificacion)
        header = lector.fieldnames
        for fila in lector:
            if fila and any(fila.values()):
                datos.append(fila)
  
    opcion=1
    while(opcion!=0):
        opcion=int(input('Quieres agregar un registro? 1=si, 0=no: '))

        if(opcion==0):
            break

        else:
          nuevo=crear_registro_vacio(header)

          for columna in nuevo.keys():
            valor = input(f'Ingrese el valor en la columna [{columna}]: ') 
            nuevo[columna] = valor 

          final={} 
          for columna in header:
              if columna in nuevo:
                  final[columna]=nuevo[columna] 
              else:
                  final[columna]=input("ingrese un id: ")  
          datos.append(final)
          agregados += 1
  
    fm.asegurar_directorio(ruta_processed)
    with open(ruta_processed, 'w', newline='', encoding='utf-8') as archivo_salida:
        escribir = csv.DictWriter(archivo_salida, fieldnames=header, lineterminator=terminator,extrasaction='ignore')
        if not os.path.isfile(ruta_processed) and os.path.getsize(ruta_processed) == 0:
           escribir.writeheader()
        escribir.writerows(datos)
    
    print(f"Archivo guardado en: {ruta_processed}")
    operacion="INSERT"
    serealizo="SI"
    re.registro_cambio_operations(ruta_operations,ruta_raw,operacion,agregados,serealizo)