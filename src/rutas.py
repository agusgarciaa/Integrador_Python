import src.file_manager as fm

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