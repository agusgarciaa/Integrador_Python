import csv
import os

from datetime import datetime

import src.helpers as hp
import src.registros as re
import src.lecturas as le

# --------------------------------------------------------------- Ejercicios 3 - Validación y calidad de datos --------------------------------------------------------------
#funcion 3a sofia martins
def verificar_coordenada(ruta_raw, separador,ruta_operations):
    """verifica si las cordenadas decimallatitude y decimallongitude estan dentro del rango valido,
       las que no cumple se agregan a una lista
       se retorna la lista y la cantidad de elementos"""
    try:
      nocumplen=[]
      with open(ruta_raw, mode='r', encoding='utf-8') as archivo:
          leer = csv.DictReader(archivo,delimiter=separador)

          for fila in leer:
              latitud=fila.get('decimalLatitude')
              longitud=fila.get('decimalLongitude')
        
              aux1=hp.verificar_latitud(latitud)
              aux2=hp.verificar_longitud(longitud)

              if not aux1 or not aux2:
                  nocumplen.append(fila)
               
      return nocumplen,len(nocumplen)
    except Exception as e:
        re.registro_cambio_operations(ruta_operations,ruta_raw,"VALIDATION",0,"ERROR")
        return [],0


#funcion 3b sofia martins
def cordenadas_faltantes(fila):
    """
    verifica si en una fila falta una de las cordenadas decimallatitude o decimallongitude, si falta una devuelve un booleano
    """
    lat = fila.get('decimalLatitude')
    lon = fila.get('decimalLongitude')
    
    if (lat != "" and lat is not None) and (lon == "" or lon is None):
        return "FALTA_LONGITUD"
    
    if (lon != "" and lon is not None) and (lat == "" or lat is None):
        return "FALTA_LATITUD"
    
    return True


# Funcion para el ejercicio 3.C - Fe Cordoba
def chequear_fecha(valor):
    """
    Intenta convertir un string a fecha usando distintos formatos.
    Retorna un objeto datetime si es válido, o None si no lo es.
    """

    if valor is None or str(valor).strip() == "":
        return None

    valor = str(valor).strip()

    formatos = [
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%y-%m-%d",
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

# Ejercicio 3.C - Fe Cordoba
def validar_fechas(ruta, ruta_operations, separador=","):
    fechas_invalidas = {} 
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

                fecha = chequear_fecha(valor)

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

    re.registro_cambio_operations(ruta_operations,ruta,operacion,cant_invalidos,'ERROR')

    return fechas_invalidas

# Ejercicio 3.D - Ana Freitas
def detectar_registros_duplicados(ruta, separador, columna):
    """
    Lee un archivo y extrae una columna específica para identificar valores repetidos.
    """
    with open(ruta, encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        header = next(lector)

        indice = hp.obtener_indice(header, columna)
        lista = [line[indice] for line in lector if len(line) > indice] 

    return hp.detectar_duplicados(lista)


# Ejercicio 3.E - Fe Cordoba
def validar_country_code(ruta, ruta_operations, separador=","):
    cods_invalidos = {}  # {fila: [(columna, valor, motivo)]}
    codigos_validos = ['AR','BO','BR','PY','UY','CL']
    operacion = 'VALIDATION'
    cant_invalidos = 0

    with open(ruta, encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        header = next(lector)

        if "countryCode" not in header:
            print("No existe la columna 'countryCode' en el dataset")
            print("Se mostrara en pantalla un diccionario vacio")
            re.registro_cambio_operations(ruta_operations, ruta, operacion, 0, 'ERROR')
            return cods_invalidos
            
        indice = header.index("countryCode")

        for num_fila, fila in enumerate(lector, start=1):
            valor = fila[indice] if indice < len(fila) else ""

            motivo = validar_country_code_registro(valor, codigos_validos)

            if motivo:
                cods_invalidos.setdefault(num_fila, []).append(
                    ("countryCode", valor, motivo)
                )
                cant_invalidos += 1
    
    re.registro_cambio_operations(ruta_operations, ruta, operacion, cant_invalidos, 'ERROR')

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
    try:
        with open(path, mode='r', encoding=c_encoding) as archivo:
            lector = csv.DictReader(archivo,delimiter=c_delimiter)
            try:
                for elemento in lector:
                    try:
                        e = elemento[campo]
                        if float(e)<0 or float(e)>valor_alto:
                            res.append(True)
                        else:
                            res.append(False)
                    except ValueError:
                        res.append(True)
            except KeyError:
                print('El dataset no contiene el campo "coordinateUncertaintyInMeters".')

    except FileNotFoundError:
        print('No se encontró el archivo. ')
            
    return res



# Ejercicio 3.G - Agustin Garcia
def calidad_dataset (ruta, ruta_operations, id, separador=","):
    total = le.total_registros(ruta, separador)
    _, coordenadas_invalidas = verificar_coordenada(ruta, separador, ruta_operations) 
    fechas_invalidas = validar_fechas(ruta, ruta_operations, separador)
    cant_fechas_invalidas = len(fechas_invalidas)
    _, duplicados, _, _ = detectar_registros_duplicados(ruta, separador, id)
    taxonomia_incompleta = hp.contar_taxonomia_incompleta(ruta, separador)

    resumen = {
        "total_registros": total,
       "coordenadas_invalidas": coordenadas_invalidas,
        "fechas_invalidas": cant_fechas_invalidas,
        "duplicados": duplicados,
        "taxonomia_incompleta": taxonomia_incompleta
    }

    reporte = f"""
    RESUMEN DE CALIDAD DEL DATASET
    -------------------
    Total: {total}
    Coordenadas inválidas: {coordenadas_invalidas}
    Fechas inválidas: {cant_fechas_invalidas}
    Duplicados: {duplicados}
    Taxonomía incompleta: {taxonomia_incompleta}
    """.strip()

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

        se usan las librerías: csv, utils
    """
    ret = []
    columnas_lat = ['decimalLatitude','latitudeDecimal']
    columnas_long = ['decimalLongitude','longitudeDecimal']
    lat_key= None
    long_key = None
    try:
        with open(path,mode='r',encoding=c_encoding) as archivo:
            lector = csv.DictReader(archivo,delimiter=c_delimiter)
            for col in columnas_lat:
                if (col in lector.fieldnames):
                    lat_key=col
                    break
            for col in columnas_long:
                if (col in lector.fieldnames):
                    long_key=col
                    break
            
            if (lat_key is None):
                print('No se encontró una latitud.')
            if (long_key is None):
                print('No se encontró una longitud.')

            if (lat_key is not None) and (long_key is not None):
                for elemento in lector:
                    dat_lat = elemento[lat_key]
                    dat_long = elemento[long_key]
                    
                    res_lat = hp.check_coordenadas(dat_lat,hp.MAX_LAT,hp.MIN_LAT)
                    res_long = hp.check_coordenadas(dat_long,hp.MAX_LONG,hp.MIN_LONG)
                    
                    ret.append((res_lat,res_long))
    except FileNotFoundError:
        print('No se encontró el archivo. ')

    return ret


# Funcion 3.I - Ana Freitas
def validar_campo_latitud(fila):
    """
    Agrupa todas las validaciones específicas para el campo de latitud.
    Verifica rango global, pertenencia a Sudamérica e integridad de datos.
    """
    lat = fila.get('decimalLatitude') or fila.get('latitudeDecimal')

    if lat is None:
        return False
    
    es_valida = (hp.verificar_latitud(lat) and hp.check_coordenadas(lat, hp.MAX_LAT, hp.MIN_LAT) and cordenadas_faltantes(fila) != "FALTA_LATITUD")
    return es_valida


# Funcion 3.I - Ana Freitas
def validar_campo_longitud(fila):
    """
    Agrupa todas las validaciones específicas para el campo de longitud.
    Verifica rango global, pertenencia a Sudamérica e integridad de datos.
    """
    lon = fila.get('decimalLongitude') or fila.get('longitudeDecimal')

    if lon is None:
        return False
    
    es_valida = (hp.verificar_longitud(lon) and hp.check_coordenadas(lon, hp.MAX_LONG, hp.MIN_LONG) and cordenadas_faltantes(fila) != "FALTA_LONGITUD")
    return es_valida


# Funcion de apoyo para el ejercicio 6.E - Ana Freitas
def es_registro_valido(fila, indices, codigos_validos):
    """
    Agrupa todas las validaciones de la sección 3.
    Retorna una tupla True,'Válido' si el registro está limpio, False,'<motivo del conflicto>' si es conflictivo.
    """

    if not validar_campo_latitud(fila):
        return (False,'Latitud')
    if not validar_campo_longitud(fila):
        return (False,'Longitud')

    columnas_a_validar = ['eventdate', 'verbatimeventdate']

    for nombre_columna in columnas_a_validar:
            valor_fecha = fila.get(nombre_columna)
            
            if valor_fecha is not None and valor_fecha != "":
                fecha_convertida = chequear_fecha(valor_fecha)
                if fecha_convertida is None or fecha_convertida > datetime.now():
                    return (False,'Fecha')

    identificador_unico = fila.get('occurrenceID')
    if identificador_unico in indices:
        return (False, 'ID')
    indices.add(identificador_unico)

    codigo_pais = fila.get('countryCode')
    if codigo_pais and validar_country_code_registro(codigo_pais, codigos_validos):
        return (False,'País')

    incertidumbre_metros = fila.get('coordinateUncertaintyInMeters')
    if incertidumbre_metros:
        try:
            val = float(incertidumbre_metros)
            if val < 0 or val > 100:
                return (False,'Coordenada')
        except ValueError:
            return (False,'Valor')

    return (True,'Válido')


# Funcion de apoyo para el 3.C - Fe Cordoba 
def validar_country_code_registro(valor, codigos_validos):
    if valor is None:
        return "nulo"
    
    valor = valor.strip()

    if valor == "" or valor.lower() == "n/a":
        return "nulo"
    
    if valor not in codigos_validos:
        return "código inválido"
    
    return None


def validar(**kwargs):
    ret = {}

    paises_permitidos = ['AR', 'BO', 'BR', 'PY', 'UY', 'CH']

    for columna, valor in kwargs.items():
        # Por defecto, si no conocemos la columna, la consideramos válida
        # para no bloquear la edición de campos simples (ej. nombres, notas).
        ret[columna] = True 

        match columna:
            # Validación de Coordenadas
            case 'decimalLatitude' | 'latitudeDecimal':
                ret[columna] = hp.check_coordenadas(valor, hp.MAX_LAT, hp.MIN_LAT)

            case 'decimalLongitude' | 'longitudeDecimal':
                ret[columna] = hp.check_coordenadas(valor, hp.MAX_LONG, hp.MIN_LONG)

            # Validación de Fechas
            case 'eventdate' | 'verbatimeventdate':
                # Asumimos que chequear_fecha devuelve un objeto fecha o None
                aux = chequear_fecha(valor)
                ret[columna] = (aux is not None)

            # Validación de Código de País
            case 'countryCode':
                # Según tu lógica: retorna "nulo" o "código inválido" si falla
                aux = validar_country_code_registro(valor, paises_permitidos)
                if aux in ["nulo", "código inválido"]:
                    ret[columna] = False
                else:
                    ret[columna] = True

            # Caso por defecto (opcional si ya inicializaste en True arriba)
            case _:
                ret[columna] = True

    return ret