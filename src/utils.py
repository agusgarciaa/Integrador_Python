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
    with open(path, mode='r', encoding=c_encoding) as file:
        lector = csv.reader(file, delimiter=c_delimiter)
        header = next(lector)
        for index, column in enumerate(header):
            dict_index[column] = index
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
def value_frequency (path,name,c_delimiter=',',c_encoding='utf-8'):
    """
        Recibe el path de un archivo en formato csv y lo lee.
        Devuelve un diccionario que tiene como clave el nombre del VALOR de la columna y como valor la cantidad de veces que aparece repetido.
        Parametros:
            path: un path (mejor si es un r-string)
            c_delimeter: por defecto seteado en ',' indica el delimeter al leer el archivo con csv.reader()
            c_encoding: por defecto seteado en 'utf-8' indica el encoding al abrir el archivo con open()

        se usan las librerias: csv, collections(Counter)
    """
    freq = Counter()
    name = str(name)
    with open(path, mode='r', encoding=c_encoding) as file:
        lector = csv.reader(file, delimiter=c_delimiter)
        header = next(lector)
        match name.isdigit():
            case True:
                #name es el numero de la columna
                name = int(name)
                for element in lector:
                    freq[element[name]]+= 1
            case False:
                #name es el nombre de la columna
                if name in header:
                    pos = header.index(name)
                    for element in lector:
                        freq[element[pos]]+= 1
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

def verificar_coordenada(rarchivo):
    nocumplen=[]
    with open(rarchivo, mode='r', encoding='utf-8') as archivo:
        leer = csv.DictReader(archivo)

        for fila in leer:
            latitud=fila.get('decimalLatitude')
            longitud=fila.get('decimalLongitude')
            aux=False
        
            if not hp.numero(latitud)or not hp.numero(longitud):
                 aux=True
            else:
                  aux1=float(latitud)
                  aux2=float(longitud)
                  if not -90<=aux1<=90 or not -180<=aux2<=180:
                     aux=True

            if aux:
                nocumplen.append(fila)
               
    return nocumplen,len(nocumplen)


#funcion 3b sofia martins
def cordenadas_faltantes(rarchivo,delimiterr):
    invalidos=[]
    with open(rarchivo, mode='r', encoding='utf-8') as archivo:
        leer=csv.DictReader(archivo, delimiter=delimiterr)
        encabezado=leer.fieldnames
   
        for fila in leer:
            aux1=fila.get('decimalLatitude') 
            aux2=fila.get('decimalLongitude') 
            id=fila.get('id') or fila.get('gbifID') or fila.get('occurrenceID') 
      
            if (aux1=="" and aux2!="") or (aux1!="" and aux2==""):
                lista=[]
                lista=[id,aux1,aux2]
                invalidos.append(lista)
    
    return invalidos


# Ejercicio 3.C - Fe Cordoba
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

                elif fecha > datetime.now():
                    fechas_invalidas.setdefault(num_fila, []).append(
                        (header[i], valor, "fecha futura")
                    )

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
def validar_country_code(ruta, separador=","):
    cods_invalidos = {}  # {fila: [(columna, valor, motivo)]}
    codigos_validos = ['AR','BO','BR','PY','UY','CH']

    with open(ruta, encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        header = next(lector)

        if "countryCode" not in header:
            raise ValueError("No existe la columna 'countryCode' en el dataset")

        indice = header.index("countryCode")

        for num_fila, fila in enumerate(lector, start=1):

            valor = fila[indice].strip() if indice < len(fila) else ""

            if valor == "" or valor.lower() == "n/a":
                cods_invalidos.setdefault(num_fila, []).append(
                    ("countryCode", valor, "nulo")
                )

            elif valor not in codigos_validos:
                cods_invalidos.setdefault(num_fila, []).append(
                    ("countryCode", valor, "código inválido")
                )

    return cods_invalidos


# Ejercicio 3.G - Agustin Garcia
def calidad_dataset (ruta, separador=","):
    total = total_registros(ruta, separador)
    # with open(ruta, encoding="utf-8") as dataset:
    #     _, coordenadas_invalidas = funcion3a(dataset)   ---> Sacar comentario cuando se solucione.
    # fechas_invalidas = validar_fechas(ruta, separador)  ---> Sacar comentario cuando se solucione.
    # cant_fechas_invalidas = len(validar_fechas)
    _, duplicados, _, _ = detectar_registros_duplicados(ruta, separador, "occurrenceID")
    taxonomia_incompleta = hp.contar_taxonomia_incompleta(ruta, separador)

    resumen = {
        "total_registros": total,
        # "coordenadas_invalidas": coordenadas_invalidas,
        # "fechas_invalidas": cant_fechas_invalidas,
        "duplicados": duplicados,
        "taxonomia_incompleta": taxonomia_incompleta
    }

    reporte = f"""
    RESUMEN DE CALIDAD DEL DATASET
    -------------------
    Total: {total}
    Coordenadas inválidas: {0}
    Fechas inválidas: {0}
    Duplicados: {duplicados}
    Taxonomía incompleta: {taxonomia_incompleta}
    """

    return resumen, reporte


# Ejercicio 3.F - Lucia Cipolla
def detect_uncertainty (path,c_delimiter=',',c_encoding='utf-8',high_val=100):
    """
        Recibe el path de un archivo en formato csv y lo lee.
        Devuelve una lista con un valor binario True en caso de que se detecte que el valor es negativo, mayor que la variable high_val o no numérico.
        Parametros:
            path: un path (mejor si es un r-string)
            c_delimeter: por defecto seteado en ',' indica el delimeter al leer el archivo con csv.reader()
            c_encoding: por defecto seteado en 'utf-8' indica el encoding al abrir el archivo con open()
            high_val: por defecto seteado en 100 indica cuánto se considera una gran incertidumbre

        se usan las librerias: csv, utils
    """
    res = []
    field='coordinateUncertaintyInMeters'
    with open(path, mode='r', encoding=c_encoding) as file:
        lector = csv.reader(file,delimiter=c_delimiter)
        header = next(lector)
        index_dict = column_index(path,c_delimiter,c_encoding)
        try:
            x = index_dict[field]
            for i,element in enumerate(lector):
                try:
                    e = element[x]
                    if float(e)<0 or float(e)>high_val:
                        res.append(True)
                    else:
                        res.append(False)
                except ValueError:
                    res.append(True)
        except KeyError:
            print('El dataset no contiene el campo "coordinateUncertaintyInMeters".')
            
    return res



# Ejercicio 3.F - Lucia Cipolla
def latam_coordinate_delimiter (path,c_delimiter=',',c_encoding='utf-8'):
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
    with open(path,mode='r',encoding=c_encoding) as file:
        lector = csv.reader(file,delimiter=c_delimiter)  #lector es de tipo <class '_csv.reader'>
        header = next(lector)
        aux = column_index(path,c_delimiter)
        try:
            lat = aux['decimalLatitude']
        except KeyError:
            print('decimalLatitude no se encontró. ')
            lat = None
        try:
            long = aux['decimalLongitude']
        except KeyError:
            print('decimalLongitude no se encontró. ')
            long = None

        if (lat is not None) and (long is not None):
            for i,element in enumerate(lector):
                dat_lat = element[lat]
                dat_long = element[long]
                
                try:
                    dat_lat = float(dat_lat.strip())
                    
                    if dat_lat<MIN_LAT or dat_lat>MAX_LAT:
                        res_lat = False
                    else:
                        res_lat = True

                except ValueError:
                    res_lat = False

                try:
                    dat_long = float(dat_long.strip())
                    
                    if dat_long<MIN_LONG or dat_long>MAX_LONG:
                        res_long = False
                    else:
                        res_long = True
                except ValueError:
                    res_long = False
                
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

#  Ejercicio 4.A - Fe Cordoba
def crear_registro_vacio(columnas):
    columnas_id = ["id", "occurrenceid", "gbifid"]
    
    registro = {}
    for col in columnas:
        if col.strip().lower() not in columnas_id:  
            registro[col] = None

    return registro


#funcion 4f sofia martins
def agregar_registro(ruta_raw, ruta_processed, ruta_operations):
    nuevo = {}
    datos = []
    agregados=0
     #abrimos el archivo para leerlo,con sniffer obtenemos el delimitador que usa el archivo para usarlo mas adelante
    with open(ruta_raw, 'r', newline='', encoding='utf-8') as f:
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
    for columna in header:
        valor = input(f'Ingrese el valor en la columna [{columna}]: ') 
        nuevo[columna] = valor        
    datos.append(nuevo)
    agregados +=1
    #guardamos en pc el archivo nuevo con el registro agregado,usamos el delimitador para que todo quede delimitado como estaba originalmente
    with open(ruta_processed, 'w', newline='', encoding='utf-8') as archivo2:
        escribir = csv.DictWriter(archivo2, fieldnames=header, lineterminator=terminator,extrasaction='ignore')
        escribir.writeheader()
        escribir.writerows(datos)
    
    print(f"Archivo guardado en: {ruta_processed}")
    nombredataset=Path(ruta_raw).name
    operacion="INSERT"
    registro_cambio_operations(ruta_operations,nombredataset,operacion,agregados)


#funcion4g sofia martins
def agregar_varios_registros(ruta_raw,ruta_processed,ruta_operations):  
    nuevo = {}
    datos = []
    agregados=0
     #abrimos el archivo para leerlo,con sniffer obtenemos el delimitador que usa el archivo para usarlo mas adelante
    with open(ruta_raw, 'r', newline='', encoding='utf-8') as f:
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
        nuevo={}
        opcion=int(input('quieres agregar un registro?1=si,0=no: '))
        if(opcion==0):
            break
        else:
          for columna in header:
            valor = input(f'Ingrese el valor en la columna [{columna}]: ') 
            nuevo[columna] = valor        
          datos.append(nuevo)
          agregados += 1
    #guardamos en pc el archivo nuevo con el registro agregado,usamos el delimitador para que todo quede delimitado como estaba originalmente
    with open(ruta_processed, 'w', newline='', encoding='utf-8') as archivo2:
        escribir = csv.DictWriter(archivo2, fieldnames=header, lineterminator=terminator,extrasaction='ignore')
        escribir.writeheader()
        escribir.writerows(datos)
    
    print(f"Archivo guardado en: {ruta_processed}")
    nombredataset=Path(ruta_raw).name
    operacion="INSERT"
    registro_cambio_operations(ruta_operations,nombredataset,operacion,agregados)
    
    
    # --------------------------------------------------------------- Ejercicios 6 - Eliminación de registros en datasets --------------------------------------------------------------
    
    def eliminar_por_identificador(ruta_raw,ruta_processed,ruta_operations):
      datos=[]
      se_encontro=False
      eliminados=0
      operacion="DELETE"
      #abrimos el archivo para leerlo,con sniffer obtenemos el delimitador que usa el archivo para usarlo mas adelante
      with open(ruta_raw, 'r', newline='', encoding='utf-8') as archivo:
         aux = archivo.read(512)
         aux2 = csv.Sniffer().sniff(aux)
         terminator = aux2.lineterminator
         archivo.seek(0)
         #guardamos el archivo en una estructura para eliminarle el registro
         lector = csv.DictReader(archivo, dialect=aux2)
         header = lector.fieldnames
         for fila in lector:
             if fila and any(fila.values()):
                 datos.append(fila)
         identificador=input("ingrese el identificador del registro a eliminar: ")
         for fila in datos:
             if fila.get('gbifID')==identificador or fila.get('id')==identificador or fila.get('occurrenceID') ==identificador:
                 datos.remove(fila)
                 se_encontro=True
                 eliminados += 1
                 print("se elimino el registro")
                 break
         if not se_encontro:
             print("ese identificador no estaba en el registro")

    #guardamos en pc el archivo nuevo con el registro eliminado,usamos el delimitador para que todo quede delimitado como estaba originalmente
      if se_encontro:
         with open(ruta_processed, 'w', newline='', encoding='utf-8') as archivo2:
              escribir = csv.DictWriter(archivo2, fieldnames=header, lineterminator=terminator,extrasaction='ignore')
              escribir.writeheader()
              escribir.writerows(datos)
         print(f"Archivo guardado en: {ruta_processed}")
         serealizo='SI'
      else:
         serealizo="ERROR"
    
      print(f"archivos eliminados: {eliminados}")
      nombredataset=Path(ruta_raw).name
      registro_cambio_operations(ruta_operations,nombredataset,operacion,eliminados,serealizo)


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



# --------------------------------------------------------------- Ejercicios 7 - Registro de operaciones en datasets --------------------------------------------------------------

# Ejercicio 7.A - Fe Cordoba
from datetime import datetime

def obtener_fecha_hora_actual():
    ahora = datetime.now()
    fecha_formateada = ahora.strftime("%Y-%m-%d %H:%M:%S")
    return fecha_formateada

# Ejercicio 7b - sofia martins
def registro_cambio_operations(ruta_operations,nombredataset,operacion,afectados,serealizo):
    fecha=obtener_fecha_hora_actual()
    if serealizo=='SI':
        cadena=f"{fecha} | {nombredataset} | {operacion} | {afectados} registros\n"
    if serealizo=="ERROR":
        cadena=f"{fecha} | {nombredataset} | {operacion} | {afectados} registros |ERROR\n"
    with open(ruta_operations,'a',encoding='utf-8',newline='') as archivo:
        archivo.write(cadena)
