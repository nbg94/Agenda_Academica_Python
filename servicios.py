
import colores
import persistencia
from persistencia import NOMBRE_ARCHIVO_DATOS

# =================================================================
# 1. ESTRUCTURAS DE DATOS GLOBALES
# =================================================================

# Variable para generar IDs únicos y secuenciales
_PROXIMO_ID = 1

# Una LISTA de diccionarios 
# Esta es nuestra "Base de Datos" principal.
DATOS_AGENDA = []

# Un DICCIONARIO índice 
# Mapea el ID (único) a la POSICIÓN (índice) en la lista DATOS_AGENDA
# { id_item: posicion_en_lista }
INDICE_AGENDA = {}

# Una TUPLA para datos inmutables 
# Usaremos tuplas para validar las asignaturas permitidas y los tipos de ítems.
ASIGNATURAS_PERMITIDAS = ('PYTHON', 'ACCESO A DATOS', 'SISTEMAS', 'INTERFACES', 'PROGRAMACION')
TIPOS_VALIDOS = ('TAREA', 'EXAMEN')
RANGOS_NOTA = (0.0, 10.0)

# Un CONJUNTO para evitar duplicados
# Almacena las asignaturas que SÍ tienen datos registrados.
# Se actualiza automáticamente para saber qué asignaturas están en uso.
ASIGNATURAS_ACTIVAS = set()


# =================================================================
# 2. FUNCIONES AUXILIARES INTERNAS 
# =================================================================

def _obtener_proximo_id() -> int:
    """
    Devuelve el siguiente ID único y lo incrementa para el próximo uso.
    
    :return: El ID (int) que se debe asignar al nuevo ítem.
    """
    global _PROXIMO_ID
    current_id = _PROXIMO_ID
    _PROXIMO_ID += 1

    return current_id

def _actualizar_estructuras_auxiliares():
    """
    Recalcula el DICCIONARIO ÍNDICE y el CONJUNTO de asignaturas activas.
    
    Esta función se debe llamar SIEMPRE después de un ALTA o una BAJA
    para mantener la integridad de los datos.
    """
    global INDICE_AGENDA, ASIGNATURAS_ACTIVAS
    
    # Limpiamos las estructuras para regenerarlas desde cero
    INDICE_AGENDA.clear()
    ASIGNATURAS_ACTIVAS.clear()
    
    # Recorremos la lista de datos principal para construir los auxiliares
    for indice, item in enumerate(DATOS_AGENDA):
        
        # 1. Poblamos el DICCIONARIO ÍNDICE
        item_id = item['id']
        INDICE_AGENDA[item_id] = indice
        
        # 2. Poblamos el CONJUNTO de asignaturas activas
        ASIGNATURAS_ACTIVAS.add(item['asignatura'].upper())


# =================================================================
# 3. LÓGICA DE NEGOCIO PURA (CRUD)
# =================================================================

def alta_item_logica(dni: str, nombre: str, asignatura: str, tipo: str, desc: str, nota: float | None) -> bool:
    """
    Registra un nuevo ítem (tarea o examen) en la base de datos (DATOS_AGENDA).
    Esta es la "Lógica Pura": recibe parámetros y manipula el estado global.
    
    :param dni: DNI del alumno (ej. "12345678A").
    :param nombre: Nombre del alumno (ej. "Juan Pérez").
    :param asignatura: Asignatura (ej. "PYTHON").
    :param tipo: Tipo de ítem (ej. "TAREA").
    :param desc: Descripción (ej. "PEC 1").
    :param nota: Puntuación (ej. 8.5 o None).
    :return: True si el alta fue exitosa, False si falló la validación interna.
    """
    global DATOS_AGENDA
    
    # Usamos una bandera para verificar todas las condiciones
    es_valido = True
    
    # 1. Validación interna de parámetros
    if asignatura.upper() not in ASIGNATURAS_PERMITIDAS:
        print(f"{colores.C_ROJO}Error Lógico: Asignatura '{asignatura}' no permitida.{colores.C_FIN}")
        es_valido = False
        
    if tipo.upper() not in TIPOS_VALIDOS:
        print(f"{colores.C_ROJO}Error Lógico: Tipo '{tipo}' no permitido.{colores.C_FIN}")
        es_valido = False

    # 2. Ejecución que solo ocurre si es válido
    if es_valido:
        # 2.1. Generar ID único
        nuevo_id = _obtener_proximo_id()
        
        # 2.2. Crear el diccionario (el "paquete" de datos o "ítem")
        nuevo_item = {
            'id': nuevo_id,
            'dni': dni.strip(),
            'nombre': nombre.strip(),
            'asignatura': asignatura.upper(),
            'tipo': tipo.upper(),
            'desc': desc.strip(),
            'nota': nota
        }
        
        # 2.3. Guardar y Actualizar
        DATOS_AGENDA.append(nuevo_item)
        _actualizar_estructuras_auxiliares()
        
    return es_valido # Retorno 

def listar_todos_los_items() -> list[dict]:
    """
    Devuelve la lista completa de todos los ítems de la agenda.
    (Cumple el requisito de recorrido simple para Listas de diccionarios).
    
    :return: Una copia de DATOS_AGENDA para evitar modificaciones externas directas.
    """
    # Recorrido simple sobre DATOS_AGENDA. Devolvemos una copia
    return list(DATOS_AGENDA)


def buscar_por_id(item_id: int) -> tuple[dict | None, int | None]:
    """
    Busca un ítem por su ID usando el índice para eficiencia.
    
    :param item_id: ID único del ítem a buscar.
    :return: Una tupla con (el ítem encontrado o None, su índice en DATOS_AGENDA o None).
    """
    # Búsqueda eficiente usando el DICCIONARIO ÍNDICE
    indice = INDICE_AGENDA.get(item_id) 
    if indice is not None:
        # Devolvemos el ítem y su índice para operaciones posteriores (edición/eliminación)
        return DATOS_AGENDA[indice], indice
    return None, None

def buscar_nombre_por_dni(dni: str) -> str | None:
    """
    Busca en DATOS_AGENDA si un DNI ya existe y devuelve el nombre asociado.
    
    :param dni: El DNI a buscar.
    :return: El nombre (str) si se encuentra, o None si no existe.
    """
    dni_upper = dni.upper()
    nombre_encontrado = None
    
    # Recorremos la lista buscando la primera coincidencia
    for item in DATOS_AGENDA:
        if item['dni'].upper() == dni_upper:
            nombre_encontrado = item['nombre']
            # Encontramos uno, asumimos que el nombre es correcto y salimos
    
    # Devolvemos el último nombre encontrado que coincida con ese DNI
    return nombre_encontrado


def eliminar_item_logica(item_id: int) -> bool:
    """
    Elimina un ítem de la agenda.
    
    :param item_id: ID del ítem a eliminar.
    :return: True si se eliminó, False si el ID no se encontró.
    """
    pudo_eliminar = False
    item, indice = buscar_por_id(item_id) 

    if item is not None:
        # Eliminación
        DATOS_AGENDA.pop(indice)
        _actualizar_estructuras_auxiliares()
        pudo_eliminar = True
        
    return pudo_eliminar 

def editar_puntuacion_logica(item_id: int, nueva_puntuacion: float | None) -> bool:
    """
    Actualiza la puntuación de un ítem existente.
    
    :param item_id: ID del ítem a modificar.
    :param nueva_puntuacion: La nueva nota (puede ser None si se quita la nota).
    :return: True si se modificó, False si el ID no se encontró.
    """
    pudo_editar = False
    item, indice = buscar_por_id(item_id)

    if item is not None:
        # Actualización segura
        DATOS_AGENDA[indice]['nota'] = nueva_puntuacion
        pudo_editar = True
        
    return pudo_editar

def buscar_items_por_dni(dni: str) -> list[dict]:
    """
    Busca todos los ítems (tareas/exámenes) asociados a un DNI específico.
    
    :param dni: El DNI del alumno a buscar (case-insensitive).
    :return: Una lista de diccionarios con todos los ítems encontrados.
    """
    dni_upper = dni.upper()
    
    # Comprensión de listas: encuentra todos los ítems del alumno
    items_encontrados = [
        item
        for item in DATOS_AGENDA
        if item['dni'].upper() == dni_upper
    ]
    
    return items_encontrados

def filtrar_items_logica(dni: str | None, asignatura: str | None, tipo: str | None) -> list[dict]:
    """
    Filtra la lista principal de ítems (DATOS_AGENDA) basado en múltiples criterios.
    
    :param dni: El DNI a filtrar (o None para no filtrar por DNI).
    :param asignatura: La Asignatura a filtrar (o None para no filtrar).
    :param tipo: El Tipo (TAREA/EXAMEN) a filtrar (o None para no filtrar).
    :return: Una lista de diccionarios que coinciden con TODOS los filtros.
    """
    
    # Preparamos los filtros para que no sean sensibles a mayúsculas
    dni_f = dni.upper() if dni else None
    asig_f = asignatura.upper() if asignatura else None
    tipo_f = tipo.upper() if tipo else None

    # Comprensión de listas: Recorremos DATOS_AGENDA una sola vez
    resultados = [
        item for item in DATOS_AGENDA
        # Condición 1: El filtro DNI es None O el DNI del ítem coincide
        if (dni_f is None or item['dni'].upper() == dni_f)
        # Condición 2: El filtro Asignatura es None O la Asignatura coincide
        and (asig_f is None or item['asignatura'].upper() == asig_f)
        # Condición 3: El filtro Tipo es None O el Tipo coincide
        and (tipo_f is None or item['tipo'].upper() == tipo_f)
    ]
    
    return resultados

def calcular_media_alumno_asignatura(dni: str, asignatura: str) -> float | None:
    """
    Calcula la media de un alumno específico en una asignatura específica.
    (Cálculo de Media Granular)

    :param dni: DNI del alumno (case-insensitive).
    :param asignatura: Nombre de la asignatura (case-insensitive).
    :return: La media de notas o None si no hay notas válidas.
    """
    dni_upper = dni.upper()
    asig_upper = asignatura.upper()
    
    notas = [
        item['nota']
        for item in DATOS_AGENDA
        if item['dni'].upper() == dni_upper
        and item['asignatura'] == asig_upper
        and item['nota'] is not None
    ]
    
    if not notas:
        return None
        
    return sum(notas) / len(notas)

def calcular_media_general_asignatura(asignatura: str) -> float | None:
    """
    Calcula la media general de una asignatura (todos los alumnos).
    (Cálculo de Media General)
    
    :param asignatura: Nombre de la asignatura (case-insensitive).
    :return: La media de notas o None si no hay notas válidas.
    """
    asig_upper = asignatura.upper()
    
    notas = [
        item['nota'] 
        for item in DATOS_AGENDA 
        if item['asignatura'] == asig_upper and item['nota'] is not None
    ]
            
    if not notas:
        return None
    
    return sum(notas) / len(notas)

def obtener_mejor_peor_asignatura() -> dict | None:
    """
    Calcula la media de CADA asignatura y devuelve la mejor y la peor.
    (Cálculo de Máximo/Mínimo de Medias)
    
    :return: Un diccionario {'mejor': (nombre, media), 'peor': (nombre, media)} o None.
    """
    # Usamos el CONJUNTO de asignaturas activas que ya mantenemos
    if not ASIGNATURAS_ACTIVAS:
        return None

    medias_asignaturas = []
    
    # 1. Calculamos la media de cada asignatura activa
    for asignatura in ASIGNATURAS_ACTIVAS:
        media = calcular_media_general_asignatura(asignatura)
        if media is not None:
            medias_asignaturas.append((asignatura, media)) # Lista de tuplas (Nombre, Media)

    if not medias_asignaturas:
        return None
        
    # 2. Encontramos el máximo y el mínimo
    # Usamos 'key=lambda item: item[1]' para que max/min comparen por el segundo
    # elemento de la tupla (la media)
    mejor = max(medias_asignaturas, key=lambda item: item[1])
    peor = min(medias_asignaturas, key=lambda item: item[1])
    
    return {'mejor': mejor, 'peor': peor}

def obtener_estadistica_agregada_asignaturas() -> list[dict]:
    """
    Genera una estadística agregada: cuenta de tareas y exámenes por asignatura.
    (Estadística Agregada)
    
    :return: Lista de diccionarios para imprimir en tabla.
    """
    stats = {} 
    for asig_nombre in ASIGNATURAS_ACTIVAS:
        stats[asig_nombre] = {'Tareas': 0, 'Exámenes': 0}

    for item in DATOS_AGENDA:
        asig = item['asignatura']
        if asig in stats: 
            if item['tipo'] == 'TAREA':
                stats[asig]['Tareas'] += 1
            elif item['tipo'] == 'EXAMEN':
                stats[asig]['Exámenes'] += 1

    informe = []
    for asig, data in stats.items():
        informe.append({
            'Asignatura': asig.capitalize(),
            'Tareas': data['Tareas'],
            'Exámenes': data['Exámenes']
        })
    
    return informe

def guardar_datos_logica() -> bool:
    """
    Empaqueta los datos globales y llama al módulo de persistencia para guardarlos.
    
    :return: True si se guardó con éxito, False en caso de error.
    """
    global _PROXIMO_ID
    
    # Empaquetar los datos globales necesarios
    datos_a_guardar = {
        'datos_agenda': DATOS_AGENDA,
        'proximo_id': _PROXIMO_ID
    }
    
    # Llamada al módulo externo
    return persistencia.guardar_datos_a_json(datos_a_guardar)
        

def cargar_datos_logica() -> bool:
    """
    Carga los datos desde el disco usando el módulo de persistencia y actualiza
    las estructuras globales.
    
    :return: True si se cargó con éxito, False si el archivo no existe o hay un error.
    """
    global DATOS_AGENDA, _PROXIMO_ID
    
    # Llamada al módulo externo
    datos_cargados = persistencia.cargar_datos_desde_json()

    if datos_cargados is not None:
        
        # 1. Actualizar las estructuras globales principales
        DATOS_AGENDA.clear() 
        DATOS_AGENDA.extend(datos_cargados.get('datos_agenda', []))
        _PROXIMO_ID = datos_cargados.get('proximo_id', 1)
        
        # 2. Regenerar las estructuras auxiliares (ÍNDICE y CONJUNTO)
        _actualizar_estructuras_auxiliares()
        
        return True
    
    return False # El archivo no existe o falló la carga

