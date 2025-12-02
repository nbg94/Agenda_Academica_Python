import json
import os #Necesario para verificar si el archivo existe

NOMBRE_ARCHIVO_DATOS = 'datos_agenda.json'

def guardar_datos_a_json(datos_a_guardar: dict) -> bool:
    """
    Guarda un diccionario de datos en un archivo JSON en disco.
    
    :param datos_a_guardar: Diccionario que contiene las estructuras a persistir.
    :return: True si se guardó con éxito, False en caso de error.
    """
    try:
        # Usamos 'w' (write) y 'indent=4' para un formato legible
        with open(NOMBRE_ARCHIVO_DATOS, 'w', encoding='utf-8') as f:
            json.dump(datos_a_guardar, f, indent=4)
        return True
    except IOError as e:
        print(f" Error de E/S al guardar el archivo: {e}")
        return False


def cargar_datos_desde_json() -> dict | None:
    """
    Carga los datos desde el archivo JSON del disco.
    
    :return: El diccionario con los datos cargados o None si el archivo no existe o falla.
    """
    # 1. Verificar si el archivo existe (si no, devolvemos None)
    if not os.path.exists(NOMBRE_ARCHIVO_DATOS):
        return None
        
    try:
        # 2. Leer y cargar el archivo JSON
        with open(NOMBRE_ARCHIVO_DATOS, 'r', encoding='utf-8') as f:
            datos_cargados = json.load(f)
            
        return datos_cargados
        
    except json.JSONDecodeError as e:
        print(f" Error: El archivo JSON está corrupto. No se pudo cargar. {e}")
        return None
    except IOError as e:
        print(f" Error de E/S al leer el archivo: {e}")
        return None