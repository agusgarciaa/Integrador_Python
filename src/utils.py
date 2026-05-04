import csv
import os

from datetime import datetime
from collections import Counter
from pathlib import Path

import src.file_manager as fm
import src.helpers as hp
import src.validaciones as va


# Funcion para encontrar la ruta de los datasets - Ana Freitas 
def obtener_ruta_de_datos(carpeta, dataset, archivo):
    """
    Construye la ruta final hacia un archivo específico en una carpeta
    Recibe el nombre del archivo y devuelve la dirección completa como texto.
    """

    ruta = fm.obtener_raiz_proyecto()
    ruta_completa = ruta / carpeta / dataset / archivo
    
    return str(ruta_completa)

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
    """
    Coordina la extracción de una columna y delega el cálculo de métricas 
    según el tipo de dato especificado (numérico, texto o coordenadas).
    """

    with open(ruta, encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        header = next(lector)

        lista_columna = []
        
        indice = hp.obtener_indice(header, columna)

        lista_columna = [line[indice] for line in lector if len(line) > indice] 

    if tipo_dato == 'numeric':
        return hp.calcular_numericos(lista_columna)
    elif tipo_dato == 'text':
        return hp.calcular_text(lista_columna)
    elif tipo_dato == "coordinate":
        return hp.calcular_coordenada(lista_columna)
    
    
# Ejercicio 2.J - Ana Freitas
def identificar_columnas_nulas(ruta, separador):
    """
    Identifica qué columnas del dataset no tienen ningún dato cargado 
    en ninguno de los registros (están 100% vacías).
    """
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
        registro_cambio_operations(ruta_operations,ruta_raw,"VALIDATION",0,"ERROR")
        return [],0


#funcion 3b sofia martins
def cordenadas_faltantes(fila,ruta_raw,ruta_operations):
    """verifica si en una fila falta una de las cordenadas decimallatitude o decimallongitude,
       si falta una devuelve un booleano"""
    try:
      cumple=True
      aux1=fila.get('decimalLatitude') 
      aux2=fila.get('decimalLongitude') 
      
      if ((aux1==""or aux1==None) and aux2!="") or (aux1!="" and (aux2==""or aux2==None)):
           cumple=False
    
      return cumple
    except Exception as e:
        registro_cambio_operations(ruta_operations,ruta_raw,"VALIDATION",0,"ERROR")
        return False


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
            if col.strip().lower() in columnas_fecha:  # recorro columnas y si coinciden con las q busco las agrego a los indices
                indices_fecha.append(i)

        print("Columnas detectadas como fecha:")
        print([header[i] for i in indices_fecha])

        for num_fila, fila in enumerate(lector, start=1):
            for i in indices_fecha:

                # evita error si la fila tiene menos columnas
                valor = fila[i].strip() if i < len(fila) else ""

                if valor == "" or valor.lower() == "n/a":
                    continue

                fecha = va.chequear_fecha(valor)

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
    codigos_validos = ['AR','BO','BR','PY','UY','CH']
    operacion = 'VALIDATION'
    cant_invalidos = 0

    with open(ruta, encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        header = next(lector)

        if "countryCode" not in header:
            print("No existe la columna 'countryCode' en el dataset")
            print("Se mostrara en pantalla un diccionario vacio")
            registro_cambio_operations(ruta_operations, ruta, operacion, 0, 'ERROR')
            return cods_invalidos
            
        indice = header.index("countryCode")

        for num_fila, fila in enumerate(lector, start=1):
            valor = fila[indice] if indice < len(fila) else ""

            motivo = va.validar_country_code_registro(valor, codigos_validos)

            if motivo:
                cods_invalidos.setdefault(num_fila, []).append(
                    ("countryCode", valor, motivo)
                )
                cant_invalidos += 1
    
    registro_cambio_operations(ruta_operations, ruta, operacion, cant_invalidos, 'ERROR')

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
def calidad_dataset (ruta, ruta_operations, id, separador=","):
    total = total_registros(ruta, separador)
    #  _, coordenadas_invalidas = verificar_coordenada(ruta, separador) 
    fechas_invalidas = validar_fechas(ruta, ruta_operations, separador)
    cant_fechas_invalidas = len(fechas_invalidas)
    _, duplicados, _, _ = detectar_registros_duplicados(ruta, separador, id)
    taxonomia_incompleta = hp.contar_taxonomia_incompleta(ruta, separador)

    resumen = {
        "total_registros": total,
       #  "coordenadas_invalidas": coordenadas_invalidas,
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

        se usan las librrerías: csv, utils
    """
    ret = []

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
                
                res_lat = hp.check_coordenadas(dat_lat,hp.MAX_LAT,hp.MIN_LAT)
                res_long = hp.check_coordenadas(dat_long,hp.MAX_LONG,hp.MIN_LONG)
                
                ret.append((res_lat,res_long))
            
    return ret

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


#funcion 4f sofia martins
def agregar_registro(ruta_raw, ruta_processed, ruta_operations):
    """agrega un registro al dataset pidiendo los valores al usuario,
       si existe el archivo processed trabajo  sobre ese,sino con raw y guarda el resultado en processed
       usamos sniffer para imitar las caracteristicas del archivo original y guardar en el mismo formato"""
    datos = []
    agregados=0
     
    ruta_entrada = ruta_processed if os.path.exists(ruta_processed) else ruta_raw

    with open(ruta_entrada, 'r', newline='', encoding='utf-8') as f:
        muestra = f.read(512)
        codificacion = csv.Sniffer().sniff(muestra)
        terminator = codificacion.lineterminator
        f.seek(0)
        lector = csv.DictReader(f, dialect=codificacion)
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
    """agregan varios registros al dataset pidiendo los valores al usuario,
       si existe el archivo processed trabajo  sobre ese,sino con raw y guarda el resultado en processed
       usamos sniffer para imitar las caracteristicas del archivo original y guardar en el mismo formato"""
    datos = []
    agregados=0
    
    ruta_entrada = ruta_processed if os.path.exists(ruta_processed) else ruta_raw

     
    with open(ruta_entrada, 'r', newline='', encoding='utf-8') as f:
        muestra = f.read(512)
        codificacion = csv.Sniffer().sniff(muestra)
        terminator = codificacion.lineterminator
        f.seek(0)
        lector = csv.DictReader(f, dialect=codificacion)
        header = lector.fieldnames
        for fila in lector:
            if fila and any(fila.values()):
                datos.append(fila)
  
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
  
    fm.asegurar_directorio(ruta_processed)
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
    col_index = column_index(path,c_delimiter,c_encoding)

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
        registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')
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
            registro_cambio_operations(ruta_operations, ruta_raw, operacion, afectados, 'SI')
        else:
            print(f"Error: No se realizaron cambios. No existe el id: '{identificador}'")
            registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')

    except Exception as e:
        print(f"Error inesperado: {e}")
        registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')


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
        registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')
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
            registro_cambio_operations(ruta_operations, ruta_raw, operacion, afectados, 'SI')
        else:
            print(f"Error: No se encontró el registro con ID '{identificador}'")
            registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')

    except Exception as e:
        print(f"Ocurrió un error inesperado al actualizar: {e}")
        registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')


 # --------------------------------------------------------------- Ejercicios 6 - Eliminación de registros en datasets --------------------------------------------------------------
    
# Función 6.A - Sofia Martins
def eliminar_por_identificador(ruta_raw, ruta_processed, ruta_operations):
    """elimina un registro del dataset pidiendo los valores al usuario,
       si existe el archivo processed trabajo  sobre ese,sino con raw y guarda el resultado en processed
       usamos sniffer para imitar las caracteristicas del archivo original y guardar en el mismo formato"""
    datos = []
    se_encontro = False
    eliminados = 0
    operacion = "DELETE"

    ruta_entrada = ruta_processed if os.path.exists(ruta_processed) else ruta_raw

    with open(ruta_entrada, 'r', newline='', encoding='utf-8') as archivo:
        aux = archivo.read(512)
        aux2 = csv.Sniffer().sniff(aux)
        terminator = aux2.lineterminator
        archivo.seek(0)

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

    if se_encontro:
        fm.asegurar_directorio(ruta_processed)
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
    registro_cambio_operations(ruta_operations, ruta_raw, operacion, eliminados, serealizo)


# Función 6.B - Agustin Garcia
def eliminar_registros_por_valor (ruta_raw, ruta_processed, ruta_operations, columna, valores_a_eliminar, separador =","):
    """Función que elimina registros cuyo valor en una columna pertenezca a una lista
        de valores suministrada por el usuario.
    """
    valores_a_eliminar = [v.strip() for v in valores_a_eliminar]
    operacion = "DELETE"

    ruta_entrada = ruta_processed if os.path.exists(ruta_processed) else ruta_raw

    try:
        with open(ruta_entrada, encoding="utf-8") as archivo:
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

                    if fila[indice].strip() in valores_a_eliminar:
                        cant_eliminados += 1
                    else:
                        escritor.writerow(fila)

        print(f"Se eliminaron {cant_eliminados} registros.")
        registro_cambio_operations(ruta_operations, ruta_raw, operacion, cant_eliminados, 'SI')
        return cant_eliminados
    
    except Exception as e:
        print(f"Error: {e}")
        registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')
        return 0
    
    
# Ejercicio 6.C - Fe Cordoba
def eliminar_por_condicion(archivo, ruta_processed, ruta_operations, columna, condicion, valor, delimiter=","):

    """Modifica el dataset procesado eliminando ciertos registros."""

    condiciones_validas = ["==", "!=", ">", ">=", "<", "<="]
    if condicion not in condiciones_validas:
        registro_cambio_operations(ruta_operations, archivo, operacion, 0, 'ERROR')
        raise ValueError("Condición no válida")

    if valor == "" or valor == "N/A":
        registro_cambio_operations(ruta_operations, archivo, operacion, 0, 'ERROR')
        raise ValueError("El valor a comparar no puede ser vacío o 'N/A'")

    operacion = "DELETE"
    eliminados = 0

    # si existe el archivo ocurrence del dataset en processed dataset se usa ese para leer sino el raw 
    ruta_entrada = ruta_processed if os.path.exists(ruta_processed) else archivo

    with open(ruta_entrada, newline="", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in, delimiter=delimiter)
        columnas = reader.fieldnames

        if columna not in columnas:
            registro_cambio_operations(ruta_operations, ruta_entrada, operacion, 0, 'ERROR')
            raise ValueError(f"La columna '{columna}' no existe")

        filas = list(reader)  #guardo en lista el iterador ya que es peligroso leer y escribir un mismo archivo en caso de q ocurrence exista 

        fm.asegurar_directorio(ruta_processed)  # en caso de que ocurrence no exista lo creamos, sino, no pasa nada 

        with open(ruta_processed, "w", newline="", encoding="utf-8") as f_out:  # y escribimos ahi 
            writer = csv.DictWriter(f_out, fieldnames=columnas, delimiter=delimiter)
            writer.writeheader()

            for fila in filas:
                dato = fila[columna] # guardo el dato de esa columna 

                if not hp.cumple_condicion(dato, condicion, valor): # si no cumple, lo escribo en el processed
                    writer.writerow(fila)
                else:
                    eliminados += 1  # si cumple debo eliminarlo (excluirlo del processed)

    registro_cambio_operations(ruta_operations, ruta_entrada, operacion, eliminados, 'SI')


# Función 6.E - Ana Freitas
def sanitizar_dataset(ruta_raw, ruta_processed, ruta_operations, separador=','):
    """
    Sanitización automática de datasets.
    Recibe la ruta del archivo original y la ruta de destino en processed_datasets.
    """
    
    registros_sanitizados = []
    indices = set()
    operacion = "DELETE"
    eliminados = 0
    codigos_validos = ['AR', 'BO', 'BR', 'PY', 'UY', 'CH']

    ruta_entrada = ruta_processed if os.path.exists(ruta_processed) else ruta_raw

    try:
        with open(ruta_entrada, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo, delimiter=separador)
            header = lector.fieldnames

            for fila in lector:
                if va.es_registro_valido(fila, indices, codigos_validos):
                    registros_sanitizados.append(fila)
                else:
                    eliminados += 1

        fm.asegurar_directorio(ruta_processed) 
        
        with open(ruta_processed, mode='w', encoding='utf-8', newline='') as archivo_salida:
            escritor = csv.DictWriter(archivo_salida, fieldnames=header, delimiter=separador)
            escritor.writeheader()
            escritor.writerows(registros_sanitizados)
            
        print(f"Sanitización finalizada. Registros conservados: {len(registros_sanitizados)}")

        registro_cambio_operations(ruta_operations, ruta_raw, operacion, eliminados, 'SI')

    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo en {ruta_entrada}")
        registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        registro_cambio_operations(ruta_operations, ruta_raw, operacion, 0, 'ERROR')

# --------------------------------------------------------------- Ejercicios 7 - Registro de operaciones en datasets --------------------------------------------------------------

# Ejercicio 7.A - Fe Cordoba
def obtener_fecha_hora_actual():
    ahora = datetime.now()  
    fecha_formateada = ahora.strftime("%Y-%m-%d %H:%M:%S") 
    return fecha_formateada


# Ejercicio 7b - sofia martins
def registro_cambio_operations(ruta_operations,ruta_raw,operacion,afectados,serealizo):
    """registra en el archivo logs la operacion realizada y sus caracteristicas"""
    fecha=obtener_fecha_hora_actual()
    nombredataset=Path(ruta_raw).parent.name
    if serealizo=='SI':
        cadena=f"{fecha} | {nombredataset} | {operacion} | {afectados} registros\n"
    if serealizo=="ERROR":
        cadena=f"{fecha} | {nombredataset} | {operacion} | {afectados} registros |ERROR\n"
    print(serealizo)
    with open(ruta_operations,'a',encoding='utf-8',newline='') as archivo:
        archivo.write(cadena)
