from datetime import datetime
from pathlib import Path

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