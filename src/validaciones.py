from datetime import datetime

import src.helpers as hp

#funcion 3b sofia martins
def cordenadas_faltantes(fila):
    lat = fila.get('decimalLatitude')
    lon = fila.get('decimalLongitude')
    
    if (lat != "" and lat is not None) and (lon == "" or lon is None):
        return "FALTA_LONGITUD"
    
    if (lon != "" and lon is not None) and (lat == "" or lat is None):
        return "FALTA_LATITUD"
    
    return True


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