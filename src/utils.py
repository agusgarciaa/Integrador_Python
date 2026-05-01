import csv
import os

from datetime import datetime
from collections import Counter
from pathlib import Path

import src.file_manager as fm
import src.helpers as hp


# Funcion para encontrar la ruta de los datasets - Ana Freitas 
def obtener_ruta_de_datos(carpeta, dataset, archivo):
    """
    Construye la ruta final hacia un archivo específico en una carpeta
    Recibe el nombre del archivo y devuelve la dirección completa como texto.
    """

    ruta = fm.obtener_raiz_proyecto()
    ruta_completa = ruta / carpeta / dataset / archivo
    
    return str(ruta_completa)

# Funcion para encontrar la ruta de los datasets - Ana Freitas 
def obtener_ruta_log(carpeta, archivo):
    """
    Construye la ruta final hacia un archivo específico en una carpeta
    Recibe el nombre del archivo y devuelve la dirección completa como texto.
    """

    ruta = fm.obtener_raiz_proyecto()
    ruta_completa = ruta / carpeta / archivo
    
    return str(ruta_completa)

# --------------------------------------------------------------- Ejercicios 2 - Lectura del dataset --------------------------------------------------------------
   
#funcion 2a sofia martins
def recorrer_diez_filas(ruta,delimiterr):
    #abrimos el archivo con open, en modo de lectura,formato utf-8
    with open(ruta, mode='r', encoding='utf-8') as archivo:
         #nos salteamos la primera linea que es el encabezado
        next(archivo)
         #le indicaremos al lector que los campos estan separados con ese delimitador
        modo = csv.reader(archivo, delimiter=delimiterr)
         #imprimimos las primeras 10 filas, i sirve para contar por cual fila vamos
        for i, fila in enumerate(modo):
            if i < 10:
                print(fila)
            else:
                break


#funcion 2b sofia martins
def imprimir_encabezados(ruta, delimiter=','):
     #abrimos el archivo en modo lectura y con delimitador utf-8
    archivo = open(ruta, 'r', encoding='utf-8')
     #le indicamos al reader que tipo de delimitador tienen los campos
    modo = csv.reader(archivo, delimiter=delimiter)
     #imprimimos la primera linea,osea los encanbezados
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
    with open(path, mode='r', encoding=c_encoding) as archivo:
        lector = csv.reader(archivo, delimiter=c_delimiter)
        header = next(lector)
        for i, columna in enumerate(header):
            dict_index[columna] = i
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
def contar_valores_distintos (nombre_columna, ruta, separador=",", encoding="utf-8"):
    valores = []

    with open(ruta, newline='', encoding=encoding) as archivo_dataset:
        lector = csv.reader(archivo_dataset, delimiter=separador)
        header = [columna.strip() for columna in next(lector)]   # Lee la primer fila

        if nombre_columna not in header:
            print("No se encontró la columna específicada. ")
            return None
        else:
            i = header.index(nombre_columna)   # Indice para tomar la columna de manera directa
        
            for registro in lector:
                if registro[i] not in valores:   # Si el valor no fue usado por otro registro se agrega a la lista
                    valores.append(registro[i])
        
    return len(valores)   # Retorna el total de valores distintos


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
    with open(path, mode='r', encoding=c_encoding) as archivo:
        lector = csv.reader(archivo, delimiter=c_delimiter)
        header = next(lector)
        match nombre.isdigit():
            case True:
                nombre = int(nombre)
                for elemento in lector:
                    freq[elemento[nombre]]+= 1
            case False:
                if nombre in header:
                    pos = header.index(nombre)
                    for elemento in lector:
                        freq[elemento[pos]]+= 1
                else:
                    print('No se encontró la columna.')
    freq=dict(freq)
    return freq


# Ejerciico 2.I - Ana Freitas
def verificar_tipo(ruta, separador, columna, tipo_dato):

    with open(ruta, encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        header = next(lector)

        lista_columna = []
        
        indice = hp.obtener_indice(header, columna)

        lista_columna = [line[indice] for line in lector if len(line) > indice] # Guarda solo los datos de la columna deseada y salta las filas que vienen vacías o incompletas.

    if tipo_dato == 'numeric':
        return hp.calcular_numericos(lista_columna)
    elif tipo_dato == 'text':
        return hp.calcular_text(lista_columna)
    elif tipo_dato == "coordinate":
        return hp.calcular_coordenada(lista_columna)
    
    
# Ejercicio 2.J - Ana Freitas
def identificar_columnas_nulas(ruta, separador):

    with open(ruta, encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        header = next(lector)

        indices_vacios = set(range(len(header)))

        for line in lector:
            for index in list(indices_vacios):
                if index < len(line) and line[index].strip():
                    indices_vacios.remove(index)

            if not indices_vacios:
                break
    
    columnas_vacias = [header[index] for index in indices_vacios]
    return 'Columnas que solo tienen nulos: ', columnas_vacias
    

# --------------------------------------------------------------- Ejercicios 3 - Validación y calidad de datos --------------------------------------------------------------
#funcion 3a sofia martins

def verificar_coordenada(ruta, separador):
    nocumplen=[]
    with open(ruta, mode='r', encoding='utf-8', delimiter=separador) as archivo:
        leer = csv.DictReader(archivo)

        for fila in leer:
            latitud=fila.get('decimalLatitude')
            longitud=fila.get('decimalLongitude')
        
            aux1=hp.verificar_latitud(latitud)
            aux2=hp.verificar_longitud(longitud)

            if not aux1 or not aux2:
                nocumplen.append(fila)
               
    return nocumplen,len(nocumplen)


#funcion 3b sofia martins
def cordenadas_faltantes(fila):
    cumple=True
    aux1=fila.get('decimalLatitude') 
    aux2=fila.get('decimalLongitude') 
      
    if ((aux1==""or aux1==None) and aux2!="") or (aux1!="" and (aux2==""or aux2==None)):
         cumple=False
    
    return cumple


# Ejercicio 3.C - Fe Cordoba
def validar_fechas(ruta, ruta_operations, separador=","):
    fechas_invalidas = {}  # {fila: [(columna, valor, motivo)]}
    operacion = 'VALIDATION'
    cant_invalidos = 0

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

        for num_fila, fila in enumerate(lector, start=1):
            for i in indices_fecha:

                # evita error si la fila tiene menos columnas
                valor = fila[i].strip() if i < len(fila) else ""

                if valor == "" or valor.lower() == "n/a":
                    continue

                fecha = hp.chequear_fecha(valor)

                if fecha is None:
                    fechas_invalidas.setdefault(num_fila, []).append(
                        (header[i], valor, "formato inválido")
                    )
                    cant_invalidos += 1 

                elif fecha > datetime.now():
                    fechas_invalidas.setdefault(num_fila, []).append(
                        (header[i], valor, "fecha futura")
                    )
                    cant_invalidos += 1 

    registro_cambio_operations(ruta_operations,ruta,operacion,cant_invalidos,'ERROR')

    return fechas_invalidas


# Ejercicio 3.D - Ana Freitas
def detectar_registros_duplicados(ruta, separador, columna):
    with open(ruta, encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        header = next(lector)

        indice = hp.obtener_indice(header, columna)
        lista = [line[indice] for line in lector if len(line) > indice] 

    return hp.detectar_duplicados(lista)


# Ejercicio 3.E - Fe Cordoba
def validar_country_code(ruta,ruta_operations, separador=","):
    cods_invalidos = {}  # {fila: [(columna, valor, motivo)]}
    codigos_validos = ['AR','BO','BR','PY','UY','CH']
    operacion = 'VALIDATION'
    cant_invalidos = 0

    with open(ruta, encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        header = next(lector)

        if "countryCode" not in header:
            print("No existe la columna 'countryCode' en el dataset")
            print("Se mostrara en pantalla un diccionario vacio")
            registro_cambio_operations(ruta_operations,ruta,operacion,0,'ERROR')
            return cods_invalidos
            
        indice = header.index("countryCode")

        for num_fila, fila in enumerate(lector, start=1):

            valor = fila[indice].strip() if indice < len(fila) else ""

            if valor == "" or valor.lower() == "n/a":
                cods_invalidos.setdefault(num_fila, []).append(
                    ("countryCode", valor, "nulo")
                )
                cant_invalidos += 1

            elif valor not in codigos_validos:
                cods_invalidos.setdefault(num_fila, []).append(
                    ("countryCode", valor, "código inválido")
                )
                cant_invalidos += 1
    
    registro_cambio_operations(ruta_operations,ruta,operacion,cant_invalidos,'ERROR')

    return cods_invalidos


# Ejercicio 3.F - Lucia Cipolla
def detect_incertidumbre (path,c_delimiter=',',c_encoding='utf-8',valor_alto=100):
    """
        Recibe el path de un archivo en formato csv y lo lee.
        Devuelve una lista con un valor binario True en caso de que se detecte que el valor es negativo, mayor que la variable high_val o no numérico.
        Parametros:
            path: un path (mejor si es un r-string)
            c_delimeter: por defecto seteado en ',' indica el delimeter al leer el archivo con csv.reader()
            c_encoding: por defecto seteado en 'utf-8' indica el encoding al abrir el archivo con open()
            valor_alto: por defecto seteado en 100 indica cuánto se considera una gran incertidumbre

        se usan las librerias: csv, utils
    """
    res = []
    campo='coordinateUncertaintyInMeters'
    with open(path, mode='r', encoding=c_encoding) as archivo:
        lector = csv.reader(archivo,delimiter=c_delimiter)
        header = next(lector)
        indice_dict = column_index(path,c_delimiter,c_encoding)
        try:
            x = indice_dict[campo]
            for i,elemento in enumerate(lector):
                try:
                    e = elemento[x]
                    if float(e)<0 or float(e)>valor_alto:
                        res.append(True)
                    else:
                        res.append(False)
                except ValueError:
                    res.append(True)
        except KeyError:
            print('El dataset no contiene el campo "coordinateUncertaintyInMeters".')
            
    return res


# Ejercicio 3.G - Agustin Garcia
def calidad_dataset (ruta, separador=","):
    total = total_registros(ruta, separador)
    # _, coordenadas_invalidas = verificar_coordenada(ruta) 
    fechas_invalidas = validar_fechas(ruta, separador)
    cant_fechas_invalidas = len(fechas_invalidas)
    _, duplicados, _, _ = detectar_registros_duplicados(ruta, separador, "occurrenceID")
    taxonomia_incompleta = hp.contar_taxonomia_incompleta(ruta, separador)

    resumen = {
        "total_registros": total,
        # "coordenadas_invalidas": coordenadas_invalidas,
        "fechas_invalidas": cant_fechas_invalidas,
        "duplicados": duplicados,
        "taxonomia_incompleta": taxonomia_incompleta
    }

    reporte = f"""
    RESUMEN DE CALIDAD DEL DATASET
    -------------------
    Total: {total}
    Coordenadas inválidas: {0}
    Fechas inválidas: {cant_fechas_invalidas}
    Duplicados: {duplicados}
    Taxonomía incompleta: {taxonomia_incompleta}
    """

    return resumen, reporte


# Ejercicio 3.H - Lucia Cipolla
def latam_delimitador_de_coordenadas (path,c_delimiter=',',c_encoding='utf-8'):
    """
        Recibe el path de un archivo en formato csv y lo lee.
        Devuelve una lista de tuplas con valores booleanos False en caso de que las coordenadas sean inválidas y True en su defecto.
        Parametros:
            path: un path (mejor si es un r-string)
            c_delimeter: por defecto seteado en ',' indica el delimeter al leer el archivo con csv.reader()
            c_encoding: por defecto seteado en 'utf-8' indica el encoding al abrir el archivo con open()

        se usan las librrerías: csv, utils
    """
    ret = []
    MAX_LAT = 13.0
    MIN_LAT = -56.0
    MAX_LONG = -34.0
    MIN_LONG = -82.0
    with open(path,mode='r',encoding=c_encoding) as archivo:
        lector = csv.reader(archivo,delimiter=c_delimiter)
        header = next(lector)
        aux = column_index(path,c_delimiter)
        try:
            lat = aux['decimalLatitude']
        except KeyError:
            try:
                lat = aux['latitudeDecimal']
            except KeyError:
                print('No se encontró una latitud. ')
                lat = None
        try:
            long = aux['decimalLongitude']
        except KeyError:
            try:
                long = aux['longitudeDecimal']
            except KeyError:
                print('No se encontró una longitud. ')
                long = None

        if (lat is not None) and (long is not None):
            for i,elemento in enumerate(lector):
                dat_lat = elemento[lat]
                dat_long = elemento[long]
                
                res_lat = hp.check_coordenadas(dat_lat,MAX_LAT,MIN_LAT)

                res_long = hp.check_coordenadas(dat_long,MAX_LONG,MIN_LONG)
                
                ret.append((res_lat,res_long))
            
    return ret


# Ejercicio 3.I - Ana Freitas
def ejecutar_validaciones_coordenadas(ruta, separador, columna_latitud, columna_longitud):
   with open(ruta, encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        header = next(lector)
        
        indice_latitud = hp.obtener_indice(header, columna_latitud)
        indice_longitud = hp.obtener_indice(header, columna_longitud)

         
# --------------------------------------------------------------- Ejercicios 4 - Inserción de registros en datasets --------------------------------------------------------------

#  Ejercicio 4.A/B - Fe Cordoba
def crear_registro_vacio(columnas):
    columnas_id = ["id", "occurrenceid", "gbifid"]
    
    registro = {}
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
        fecha_a_verificar = hp.chequear_fecha(fecha)
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


#funcion 4f sofia martins
def agregar_registro(ruta_raw, ruta_processed, ruta_operations):
    datos = []
    agregados=0
     #abrimos el archivo para leerlo,con sniffer obtenemos el delimitador que usa el archivo para usarlo mas adelante
    if os.path.isfile(ruta_processed):
        ruta=ruta_processed
    else:
        ruta=ruta_raw
        
    with open(ruta, 'r', newline='', encoding='utf-8') as f:
        muestra = f.read(512)
        codificacion = csv.Sniffer().sniff(muestra)
        terminator = codificacion.lineterminator
        f.seek(0)
        #guardamos el archivo en una estructura para agregarle el registro nuevo
        lector = csv.DictReader(f, dialect=codificacion)
        header = lector.fieldnames
        for fila in lector:
            if fila and any(fila.values()):
                datos.append(fila)
    #creamos el registro a agregar,lo agregamos al final
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
    #guardamos en pc el archivo nuevo con el registro agregado,usamos el delimitador para que todo quede delimitado como estaba originalmente
    with open(ruta_processed, 'a', newline='', encoding='utf-8') as archivo2:
        escribir = csv.DictWriter(archivo2, fieldnames=header, lineterminator=terminator,extrasaction='ignore')
        if not os.path.isfile(ruta_processed) and os.path.getsize(ruta_processed) == 0:
           escribir.writeheader()
        escribir.writerows(datos)
    
    print(f"Archivo guardado en: {ruta_processed}")
    operacion="INSERT"
    serealizo="SI"
    registro_cambio_operations(ruta_operations,ruta_raw,operacion,agregados,serealizo)


#funcion4g sofia martins
def agregar_varios_registros(ruta_raw,ruta_processed,ruta_operations):  
    datos = []
    agregados=0
    if os.path.isfile(ruta_processed):
        ruta=ruta_processed
    else:
        ruta=ruta_raw
     #abrimos el archivo para leerlo,con sniffer obtenemos el delimitador que usa el archivo para usarlo mas adelante
    with open(ruta, 'r', newline='', encoding='utf-8') as f:
        muestra = f.read(512)
        codificacion = csv.Sniffer().sniff(muestra)
        terminator = codificacion.lineterminator
        f.seek(0)
        #guardamos el archivo en una estructura para agregarle el registro nuevo
        lector = csv.DictReader(f, dialect=codificacion)
        header = lector.fieldnames
        for fila in lector:
            if fila and any(fila.values()):
                datos.append(fila)
    #creamos el registro a agregar,lo agregamos al final
    opcion=1
    while(opcion!=0):
        opcion=int(input('quieres agregar un registro?1=si,0=no: '))
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
    #guardamos en pc el archivo nuevo con el registro agregado,usamos el delimitador para que todo quede delimitado como estaba originalmente
    with open(ruta_processed, 'a', newline='', encoding='utf-8') as archivo2:
        escribir = csv.DictWriter(archivo2, fieldnames=header, lineterminator=terminator,extrasaction='ignore')
        if not os.path.isfile(ruta_processed) and os.path.getsize(ruta_processed) == 0:
           escribir.writeheader()
        escribir.writerows(datos)
    
    print(f"Archivo guardado en: {ruta_processed}")
    operacion="INSERT"
    serealizo="SI"
    registro_cambio_operations(ruta_operations,ruta_raw,operacion,agregados,serealizo)
    

# --------------------------------------------------------------- Ejercicios 5 - Actualización de registros en datasets --------------------------------------------------------------

# Ejercicio 5.B - Ana Freitas
def actualizar_campo(ruta_raw, ruta_processed, separador, identificador, columna, nuevo_valor):
    registros_actualizados = []
    
    with open(ruta_raw, encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo, delimiter=separador)
        columnas = lector.fieldnames
        
        for fila in lector:
            if fila.get("occurrenceID") == identificador:
                fila[columna] = nuevo_valor
            
            registros_actualizados.append(fila)

    with open(ruta_processed, mode='w', encoding='utf-8', newline='') as archivo:
        escritor = csv.DictWriter(archivo, delimiter=separador, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(registros_actualizados)


# Ejercicio 5.C - Ana Freitas
def actualizar_multiples_campos(ruta_raw, ruta_processed, separador, identificador, dic_cambios):
    registros_para_guardar = []
    
    # Leer el archivo desde la ruta de origen (raw)
    with open(ruta_raw, encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo, delimiter=separador)
        columnas = lector.fieldnames
        
        for fila in lector:
            # Si encontramos el ID, actualizamos el diccionario en memoria RAM
            if fila.get("occurrenceID") == identificador:
                fila.update(dic_cambios)
            
            # Guardamos la fila modificada o no en nuestra lista 
            registros_para_guardar.append(fila)

    # Escribir el resultado en la ruta de destino la carpeta processed
    with open(ruta_processed, mode='w', encoding='utf-8', newline='') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas, delimiter=separador)
        escritor.writeheader()
        escritor.writerows(registros_para_guardar)


 # --------------------------------------------------------------- Ejercicios 6 - Eliminación de registros en datasets --------------------------------------------------------------

# Función 6.A - Sofia Martins
def eliminar_por_identificador(ruta_raw, ruta_processed, ruta_operations):
    datos = []
    se_encontro = False
    eliminados = 0
    operacion = "DELETE"

    # abrimos el archivo para leerlo, con sniffer obtenemos el delimitador
    if os.path.isfile(ruta_processed):
        ruta=ruta_processed
    else:
        ruta=ruta_raw
    with open(ruta, 'r', newline='', encoding='utf-8') as archivo:
        aux = archivo.read(512)
        aux2 = csv.Sniffer().sniff(aux)
        terminator = aux2.lineterminator
        archivo.seek(0)

        # guardamos el archivo en una estructura para eliminarle el registro
        lector = csv.DictReader(archivo, dialect=aux2)
        header = lector.fieldnames

        for fila in lector:
            if fila and any(fila.values()):
                datos.append(fila)

        identificador = input("ingrese el identificador del registro a eliminar: ")

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

    # guardamos en pc el archivo nuevo con el registro eliminado
    if se_encontro:
        with open(ruta_processed, 'a', newline='', encoding='utf-8') as archivo2:
            escribir = csv.DictWriter(
                archivo2,
                fieldnames=header,
                lineterminator=terminator,
                extrasaction='ignore'
            )
            if not os.path.isfile(ruta_processed) and os.path.getsize(ruta_processed) == 0:
                escribir.writeheader()
            escribir.writerows(datos)

        print(f"Archivo guardado en: {ruta_processed}")
        serealizo = 'SI'
    else:
        serealizo = "ERROR"

    print(f"archivos eliminados: {eliminados}")
    registro_cambio_operations(
        ruta_operations,
        ruta_raw,
        operacion,
        eliminados,
        serealizo
    )


# Ejercicio 6.B - Agustin Garcia 
def eliminar_registros_por_valor (ruta_raw, ruta_processed, columna, valores_a_eliminar, separador =","):
    """Función que elimina registros cuyo valor en una columna pertenezca a una lista
        de valores suministrada por el usuario.
    """
    valores_a_eliminar = [v.strip() for v in valores_a_eliminar]

    with open(ruta_raw, encoding="utf-8") as archivo:
        cant_eliminados = 0
        lector = csv.reader(archivo, delimiter=separador)
        header = next(lector)

        indice = hp.obtener_indice(header, columna)

        if indice is None:
            return
        
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

    print(f"Se eliminaron {cant_eliminados} registros. ")
    return cant_eliminados


# Ejercicio 6.C - Fe Cordoba
def eliminar_por_condicion(archivo, ruta_processed, ruta_operations, columna, condicion, valor, delimiter=","):

    """Modifica el dataset procesado eliminando ciertos registros."""

    condiciones_validas = ["==", "!=", ">", ">=", "<", "<="]
    if condicion not in condiciones_validas:
        raise ValueError("Condición no válida")

    if valor == "" or valor == "N/A":
        raise ValueError("El valor a comparar no puede ser vacío o 'N/A'")

    operacion = "DELETE"
    eliminados = 0

    ruta_entrada = ruta_processed if os.path.exists(ruta_processed) else archivo

    with open(ruta_entrada, newline="", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in, delimiter=delimiter)
        columnas = reader.fieldnames

        if columna not in columnas:
            raise ValueError(f"La columna '{columna}' no existe")

        filas = list(reader)

        hp.asegurar_directorio(ruta_processed)

        with open(ruta_processed, "w", newline="", encoding="utf-8") as f_out:
            writer = csv.DictWriter(f_out, fieldnames=columnas, delimiter=delimiter)
            writer.writeheader()

            for fila in filas:
                dato = fila[columna]

                if not hp.cumple_condicion(dato, condicion, valor):
                    writer.writerow(fila)
                else:
                    eliminados += 1

    registro_cambio_operations(ruta_operations, ruta_entrada, operacion, eliminados, 'SI')


# Función 6.E - Ana Freitas
def sanitizar_dataset_completo(ruta_raw, ruta_processed, separador):
    registros_limpios = []
    
    ids_vistos = set() # Usamos un set para los duplicados (3.D)
    
    with open(ruta_raw, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo, delimiter=separador)
        columnas = lector.fieldnames

# --------------------------------------------------------------- Ejercicios 7 - Registro de operaciones en datasets --------------------------------------------------------------

# Ejercicio 7.A - Fe Cordoba
def obtener_fecha_hora_actual():
    ahora = datetime.now()
    fecha_formateada = ahora.strftime("%Y-%m-%d %H:%M:%S")
    return fecha_formateada


# Ejercicio 7b - sofia martins
def registro_cambio_operations(ruta_operations,ruta_raw,operacion,afectados,serealizo):
    fecha=obtener_fecha_hora_actual()
    nombredataset=Path(ruta_raw).parent.name
    if serealizo=='SI':
        cadena=f"{fecha} | {nombredataset} | {operacion} | {afectados} registros\n"
    if serealizo=="ERROR":
        cadena=f"{fecha} | {nombredataset} | {operacion} | {afectados} registros |ERROR\n"
    with open(ruta_operations,'a',encoding='utf-8',newline='') as archivo:
        archivo.write(cadena)
