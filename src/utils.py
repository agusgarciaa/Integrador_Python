import csv


def abrir_dataset(ruta_archivo, separador, codificacion):
    """
    Función para el Ejercicio 2.A - SOFI
    Abre el archivo principal utilizando la biblioteca estándar csv.

    """
    print("hello world") 
    #funcion 2a sofia martins
def recorrer_diez_filas(ruta1,ruta2,ruta3):
    #abrimos el archivo con open, en modo de lectura,formato utf-8
    with open(ruta1, mode='r', encoding='utf-8') as archivo1:
         #nos salteamos la primera linea que es el encabezado
        next(archivo1)
         #le indicaremos al lector que los campos estan separados con ese delimitador
        modo1 = csv.reader(archivo1, delimiter='\t')
         #imprimimos las primeras 10 filas, i sirve para contar por cual fila vamos
        for i, fila in enumerate(modo1):
            if i < 10:
                print(fila)
            else:
                break

    with open(ruta2, mode='r', encoding='utf-8') as archivo2:
        next(archivo2)
        modo2 = csv.reader(archivo2, delimiter=',')
        for i, fila in enumerate(modo2):
            if i < 10:
                print(fila)
            else:
                break

    with open(ruta3, mode='r', encoding='utf-8') as archivo3:
        next(archivo3)
        modo3 = csv.reader(archivo3, delimiter=',')
        for i, fila in enumerate(modo3):
            if i < 10:
                print(fila)
            else:
                break
    archivo1.close()
    archivo2.close()
    archivo3.close()
#funcion 2b sofia martins
def imprimir_encabezados(ruta1,ruta2,ruta3):
     #abrimos el archivo en modo lectura y con delimitador utf-8
    archivo1 = open(ruta1, 'r', encoding='utf-8')
     #le indicamos al reader que tipo de delimitador tienen los campos
    modo1 = csv.reader(archivo1, delimiter='\t')
     #imprimimos la primera linea,osea los encanbezados
    print(next(modo1))
    archivo1.close()

    archivo2 = open(ruta2, 'r', encoding='utf-8')
    modo2 = csv.reader(archivo2, delimiter=',')
    print(next(modo2))
    archivo2.close()

    archivo3 = open(ruta3, 'r', encoding='utf-8')
    modo3 = csv.reader(archivo3, delimiter=',')
    print(next(modo3))
    archivo3.close()

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

#funcion 3a sofia martins
def numero(dato):
    aux=dato.strip().replace('-','',1).replace('.','',1)
    return aux.isdigit()and dato.strip() !=""

def funcion3a(archivo):
    leer=csv.dictreader(archivo)
    nocumplen=[]

    for fila in leer:
        latitud=fila['decimalLatitude']
        longitud=fila['decimalLongitude']
        
        if not numero(latitud):
            nocumplen.append(fila)
        else:
            aux1=float(latitud)
            if not -90<=aux1<=90:
               nocumplen.append(fila)
        
        if not numero(longitud):
            nocumplen.append(fila)
        else:
            aux2=float(longitud)
            if not -180<=aux2<=180:
               nocumplen.append(fila)
               
    return nocumplen,len(nocumplen)

#funcion 3b sofia martins
def funcion3b(archivo):
    leer=csv.DictReader(archivo)
    header=leer.fieldnames
    haylongitud='decimalLongitude' in header
    haylatitud='decimalLatitude' in header
    invalidos=[]
    
    if haylongitud and haylatitud:
        for fila in leer:
            aux1=fila['decimalLongitude']
            aux2=fila['decimalLatitude']
            id=fila['id']or fila['gbifID']
     
        lista=[]  
        if aux1=="" and aux2=="" or aux1=="" or aux2=="":
           lista=[id,aux1,aux2]
           invalidos.append(lista)
    
    return invalidos













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

#funcion 4f sofia martins
import os

def funcion4f(ruta_archivo):  
    nuevo = {}
    datos = []
    #creamos la carpeta destino si no esta creada
    if not os.path.exists("processed_datasets"):
        os.makedirs("processed_datasets")
     #obtenemos nombre y creamos la ruta de destino donde se guardara el archivo creado
    nombre = os.path.basename(ruta_archivo)
    destino = os.path.join("processed_datasets", nombre)
     #abrimos el archivo para leerlo,con sniffer obtenemos el delimitador que usa el archivo para usarlo mas adelante
    with open(ruta_archivo, 'r', newline='', encoding='utf-8') as f:
        aux = f.read(512)
        aux2 = csv.Sniffer().sniff(aux)
        terminator = aux2.lineterminator
        f.seek(0)
        #guardamos el archivo en una estructura para agregarle el registro nuevo
        leer = csv.DictReader(f, dialect=aux2)
        header = leer.fieldnames
        for fila in leer:
            if fila and any(fila.values()):
                datos.append(fila)
    #creamos el registro a agregar,lo agregamos al final
    for columna in header:
        valor = input(f'Ingrese el valor en la columna [{columna}]: ') 
        nuevo[columna] = valor        
    datos.append(nuevo)
    #guardamos en pc el archivo nuevo con el registro agregado,usamos el delimitador para que todo quede delimitado como estaba originalmente
    with open(destino, 'w', newline='', encoding='utf-8') as archivo2:
        escribir = csv.DictWriter(archivo2, fieldnames=header, lineterminator=terminator,extrasaction='ignore')
        escribir.writeheader()
        escribir.writerows(datos)
    
    print(f"Archivo guardado en: {destino}")

#funcion4g sofia martins
def funcion4g(ruta_archivo):  
    nuevo = {}
    datos = []
    #creamos la carpeta destino si no esta creada
    if not os.path.exists("processed_datasets"):
        os.makedirs("processed_datasets")
     #obtenemos nombre y creamos la ruta de destino donde se guardara el archivo creado
    nombre = os.path.basename(ruta_archivo)
    destino = os.path.join("processed_datasets", nombre)
     #abrimos el archivo para leerlo,con sniffer obtenemos el delimitador que usa el archivo para usarlo mas adelante
    with open(ruta_archivo, 'r', newline='', encoding='utf-8') as f:
        aux = f.read(512)
        aux2 = csv.Sniffer().sniff(aux)
        terminator = aux2.lineterminator
        f.seek(0)
        #guardamos el archivo en una estructura para agregarle el registro nuevo
        leer = csv.DictReader(f, dialect=aux2)
        header = leer.fieldnames
        for fila in leer:
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
    #guardamos en pc el archivo nuevo con el registro agregado,usamos el delimitador para que todo quede delimitado como estaba originalmente
    with open(destino, 'w', newline='', encoding='utf-8') as archivo2:
        escribir = csv.DictWriter(archivo2, fieldnames=header, lineterminator=terminator,extrasaction='ignore')
        escribir.writeheader()
        escribir.writerows(datos)
    
    print(f"Archivo guardado en: {destino}")





