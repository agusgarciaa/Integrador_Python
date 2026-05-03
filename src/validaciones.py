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
    """Agrupa todas las validaciones solo para latitud."""
    lat = fila.get('decimalLatitude') or fila.get('latitudeDecimal')
    
    es_valida = (hp.verificar_latitud(lat) and 
                 hp.check_coordenadas(lat, hp.MAX_LAT, hp.MIN_LAT) and 
                 cordenadas_faltantes(fila) != "FALTA_LATITUD")
    return es_valida


def validar_campo_longitud(fila):
    """Agrupa todas las validaciones solo para longitud."""
    lon = fila.get('decimalLongitude') or fila.get('longitudeDecimal')
    
    es_valida = (hp.verificar_longitud(lon) and 
                 hp.check_coordenadas(lon, hp.MAX_LONG, hp.MIN_LONG) and 
                 cordenadas_faltantes(fila) != "FALTA_LONGITUD")
    return es_valida


# Funcion 6.E - Ana Freitas
def es_registro_valido(fila, indices, codigos_validos):
    """
    Agrupa todas las validaciones de la sección 3.
    Retorna True si el registro está limpio, False si es conflictivo.
    """

    if not validar_campo_latitud(fila) or not validar_campo_longitud(fila):
        return False

    columnas_a_validar = ['eventdate', 'verbatimeventdate']
    for nombre_columna in columnas_a_validar:
        valor_fecha = fila.get(nombre_columna)
        if valor_fecha:
            fecha_convertida = hp.chequear_fecha(valor_fecha)
            if fecha_convertida is None or fecha_convertida > datetime.now():
                return False

    identificador_unico = fila.get('occurrenceID')
    if identificador_unico in indices:
        return False 
    indices.add(identificador_unico)

    codigo_pais = fila.get('countryCode')
    if codigo_pais and hp.validar_country_code_registro(codigo_pais, codigos_validos):
        return False

    incertidumbre_metros = fila.get('coordinateUncertaintyInMeters')
    if incertidumbre_metros:
        try:
            val = float(incertidumbre_metros)
            if val < 0 or val > 100:
                return False
        except ValueError:
            return False

    return True