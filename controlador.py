import re
import utilidades
import colores
import persistencia
from persistencia import NOMBRE_ARCHIVO_DATOS
import servicios     # Para el motor de la lógica y estructuras (altas, bajas, buscar_por_dni, etc.)
from servicios import (
    ASIGNATURAS_PERMITIDAS, TIPOS_VALIDOS, RANGOS_NOTA, DATOS_AGENDA,
    buscar_nombre_por_dni, alta_item_logica, listar_todos_los_items,
    eliminar_item_logica, buscar_items_por_dni, buscar_por_id,
    editar_puntuacion_logica, filtrar_items_logica,
    calcular_media_alumno_asignatura, calcular_media_general_asignatura,
    obtener_mejor_peor_asignatura, obtener_estadistica_agregada_asignaturas,
    guardar_datos_logica, cargar_datos_logica
)

# =================================================================
# 4. ORQUESTACIÓN GESTORA (Llamadas a utilidades.py y a Lógica Pura)
# =================================================================

# Definimos los patrones de validación aquí para que sean fáciles de modificar
PATRON_DNI = r"^\d{8}[A-Za-z]$"
PATRON_NOMBRE = r"^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$"

def iniciar_carga_automatica():
    """
    Intenta cargar datos automáticamente al inicio de la aplicación si el archivo
    de datos existe, sin pedir confirmación y mostrando un mensaje si tiene éxito.
    """
    # Llama a la lógica pura. Si devuelve True, es que cargó datos.
    if cargar_datos_logica():
        # Usamos la impresión con color para avisar al usuario
        print(f"{colores.C_AMARILLO}\n Datos cargados automáticamente desde '{NOMBRE_ARCHIVO_DATOS}'.{colores.C_FIN}")
        
    # Si devuelve False, significa que el archivo no existe o hubo un error, 
    # y el programa simplemente arranca con la agenda vacía, que es lo que queremos.


def _obtener_datos_alta() -> dict | None:
    """
    Función auxiliar para gestionar_alta. Pide todos los datos necesarios
    para un nuevo ítem usando el módulo 'utilidades'.
    
    Implementa:
    1. Validación de patrón de DNI.
    2. Auto-rellenado de nombre si el DNI ya existe.
    3. Validación de patrón de Nombre.
    
    :return: Un diccionario con todos los datos validados o None si el usuario cancela.
    """
    print(f"{colores.C_MORADO}\n--- ALTA DE NUEVO ÍTEM ---{colores.C_FIN}")
    
    # 1. DNI (Validar patrón)
    dni = utilidades.pedir_cadena_con_patron(
        mensaje=f"{colores.C_MORADO}DNI Alumno (ej. 12345678A, ENTER para cancelar): {colores.C_FIN}",
        patron_regex=PATRON_DNI,
        msj_error=f"{colores.C_ROJO}Formato DNI incorrecto. Debe ser 8 números y 1 letra.{colores.C_FIN}")
    if dni is None:
        return None

    # 2. NOMBRE (Auto-rellenado)
    nombre = None
    nombre_existente = buscar_nombre_por_dni(dni) # Lógica Pura
    
    if nombre_existente is not None:
        print(f"{colores.C_VERDE}Alumno encontrado: {nombre_existente}. Nombre auto-rellenado.{colores.C_FIN}")
        nombre = nombre_existente
    else:
        # El DNI no existía, pedimos el nombre (Validar patrón)
        nombre = utilidades.pedir_cadena_con_patron(
            mensaje=f"{colores.C_MORADO}Nombre Alumno (ENTER para cancelar): {colores.C_FIN}",
            patron_regex=PATRON_NOMBRE,
            msj_error=f"{colores.C_ROJO}El nombre solo puede contener letras y espacios.{colores.C_FIN}"
        )
        if nombre is None:
            return None

    # 3. Asignatura (Lógica existente)
    asignatura_valida = False
    asignatura = None
    while not asignatura_valida:
        asignatura = utilidades.pedir_cadena_no_vacia(f"{colores.C_MORADO}Asignatura (ENTER para cancelar): {colores.C_FIN}")
        if asignatura is None:
            return None
        
        if asignatura.upper() in ASIGNATURAS_PERMITIDAS:
            asignatura_valida = True
        else:
            print(f"{colores.C_ROJO}Error: Asignatura no válida. Permitidas: {ASIGNATURAS_PERMITIDAS}{colores.C_FIN}")
            
    # 4. Tipo Tarea/Examen 
    tipo_valido = False
    tipo = None
    while not tipo_valido:
        tipo = utilidades.pedir_cadena_no_vacia(f"{colores.C_MORADO}Tipo (Tarea/Examen, ENTER para cancelar): {colores.C_FIN}")
        if tipo is None:
            return None
            
        if tipo.upper() in TIPOS_VALIDOS:
            tipo_valido = True
        else:
            print(f"{colores.C_ROJO}Error: Tipo no válido. Debe ser: {TIPOS_VALIDOS}{colores.C_FIN}")

    # 5. Descripción
    desc = utilidades.pedir_cadena_no_vacia(f"{colores.C_MORADO}Descripción (ej. 'PEC 1', ENTER para cancelar): {colores.C_FIN}")
    if desc is None:
        return None

    # 6. Nota
    nota = utilidades.pedir_flotante_en_rango(f"{colores.C_MORADO}Nota ({RANGOS_NOTA[0]}-{RANGOS_NOTA[1]}, ENTER si no tiene nota): {colores.C_FIN}",
        RANGOS_NOTA[0],
        RANGOS_NOTA[1])

    # 7. Empaquetar los datos
    return {
        'dni': dni,
        'nombre': nombre,
        'asignatura': asignatura,
        'tipo': tipo,
        'desc': desc,
        'nota': nota
    }

def gestionar_alta():
    """
    Función de Orquestación para el ALTA.
    1. Pide los datos al usuario (usando _obtener_datos_alta).
    2. Llama a la lógica pura (alta_item_logica) con esos datos.
    3. Informa al usuario del resultado.
    """
    # 1. Recoger datos del usuario
    datos_nuevos = _obtener_datos_alta()
    
    # 2. Comprobar si el usuario canceló
    if datos_nuevos is not None:
        # 3. Llamar a la Lógica Pura
        # Usamos **datos_nuevos para desempaquetar el diccionario
        # en argumentos para la función alta_item_logica.
        if alta_item_logica(**datos_nuevos):
            print(f"{colores.C_VERDE}\nÍtem registrado con éxito.{colores.C_FIN}")
        else:
            # Esto solo saltaría si la lógica interna fallase
            print(f"{colores.C_ROJO}\nError: No se pudo registrar el ítem.{colores.C_FIN}")
    else:
        print(f"{colores.C_AMARILLO}\nAlta cancelada por el usuario.{colores.C_FIN}")


def gestionar_listado():
    """
    Orquesta la obtención y la impresión del listado completo.
    """
    # 1. Obtener la lista de datos de la lógica pura
    datos = listar_todos_los_items()
    
    # 2. Definir los encabezados de la tabla y su orden
    encabezados = ['id', 'dni', 'nombre', 'asignatura', 'tipo', 'desc', 'nota']

    print(f"{colores.C_MORADO}\n--- LISTADO COMPLETO DE ÍTEMS ---{colores.C_FIN}")

    # 3. Llamar a la utilidad para imprimir con formato tabular legible
    utilidades.imprimir_tabla(datos, encabezados)


def gestionar_eliminacion():
    """
    Orquesta la eliminación de un ítem por ID.
    """
    print(f"{colores.C_MORADO}\n--- ELIMINAR ÍTEM ---{colores.C_FIN}")
    
    # Se pide el ID usando la utilidad que permite cancelar (retorna None si está vacío)
    item_id = utilidades.pedir_entero_opcional(f"{colores.C_MORADO}ID del ítem a eliminar (ENTER para cancelar): {colores.C_FIN}")

    # 1. Comprobamos la cancelación
    if item_id is not None:
        # 2. Ejecutamos la lógica y reportamos
        if eliminar_item_logica(item_id):
            print(f"{colores.C_VERDE}\nÍtem con ID {item_id} eliminado con éxito.{colores.C_FIN}")
        else:
            print(f"{colores.C_ROJO}Error: No se encontró ningún ítem con ID {item_id} para eliminar.{colores.C_FIN}")
    else:
        print(f"{colores.C_AMARILLO}Eliminación cancelada.{colores.C_FIN}")


def gestionar_editar_puntuacion():
    """
    Orquesta la edición de la puntuación.
    Proceso: Pide DNI -> Muestra ítems -> Pide ID -> Edita Nota.
    """
    print(f"{colores.C_MORADO}\n--- EDITAR PUNTUACIÓN (Búsqueda por DNI) ---{colores.C_FIN}")

    dni = utilidades.pedir_cadena_no_vacia(f"{colores.C_MORADO}DNI del Alumno con nota a editar (ENTER para cancelar): {colores.C_FIN}")

    operacion_exitosa = False
    
    if dni is not None:
        items_alumno = buscar_items_por_dni(dni)
        
        if items_alumno:
            print(f"{colores.C_MORADO}\nSe encontraron {len(items_alumno)} ítems para el DNI '{dni.upper()}':{colores.C_FIN}")
            encabezados = ['id', 'asignatura', 'tipo', 'desc', 'nota']
            utilidades.imprimir_tabla(items_alumno, encabezados)

            item_id = utilidades.pedir_entero_opcional(f"{colores.C_MORADO}ID del ítem exacto que quieres editar (ENTER para cancelar): {colores.C_FIN}")

            if item_id is not None:
                item_a_editar, _ = buscar_por_id(item_id)
                
                if item_a_editar is not None and item_a_editar['dni'].upper() == dni.upper():
                    print(f"{colores.C_MORADO}\n Editando: {item_a_editar['desc']} de {item_a_editar['asignatura']} - Nota actual: {item_a_editar['nota']}{colores.C_FIN}")

                    nueva_puntuacion = utilidades.pedir_flotante_en_rango(
                        f"{colores.C_MORADO}Nueva Puntuación ({RANGOS_NOTA[0]}-{RANGOS_NOTA[1]}, ENTER para cancelar): {colores.C_FIN}",
                        RANGOS_NOTA[0], 
                        RANGOS_NOTA[1]
                    )

                    if nueva_puntuacion is not None:
                        operacion_exitosa = editar_puntuacion_logica(item_id, nueva_puntuacion)
                        
                        if operacion_exitosa:
                            print(f"{colores.C_VERDE}\n Puntuación del ítem {item_id} actualizada a {nueva_puntuacion:.2f}.{colores.C_FIN}")
                        else:
                            print(f"{colores.C_ROJO} Error interno al actualizar puntuación del ID {item_id}.{colores.C_FIN}")
                    else:
                        print(f"{colores.C_AMARILLO} Edición de puntuación cancelada.{colores.C_FIN}")
                else:
                    print(f"{colores.C_ROJO} Error: El ID {item_id} no existe o no pertenece al DNI {dni.upper()}.{colores.C_FIN}")
            else:
                print(f"{colores.C_AMARILLO} Selección de ítem cancelada.{colores.C_FIN}")
        else:
            print(f"{colores.C_ROJO} Error: No se encontró ningún registro para el DNI '{dni}'.{colores.C_FIN}")
    else:
        print(f"{colores.C_AMARILLO} Edición cancelada.{colores.C_FIN}")



def gestionar_filtrado_busqueda():
    """
    Orquesta la solicitud de filtros al usuario y muestra los resultados.
    Permite filtros combinados (ej. Tareas de un DNI en una Asignatura).
    """
    print(f"{colores.C_MORADO}\n--- BÚSQUEDA Y FILTRADO DE ÍTEMS --- {colores.C_FIN}")
    print(f"{colores.C_MORADO}Deja un campo vacío (ENTER) si no quieres filtrar por él. {colores.C_FIN}")

    # 1. Pedir los criterios de filtrado (usando la utilidad que devuelve None si está vacío)
    filtro_dni = utilidades.pedir_cadena_no_vacia(f"{colores.C_MORADO}Filtrar por DNI: {colores.C_FIN}")
    filtro_asig = utilidades.pedir_cadena_no_vacia(f"{colores.C_MORADO}Filtrar por Asignatura: {colores.C_FIN}")
    filtro_tipo = utilidades.pedir_cadena_no_vacia(f"{colores.C_MORADO}Filtrar por Tipo (Tarea/Examen): {colores.C_FIN}")

    # 2. Llamar a la Lógica Pura con los filtros
    resultados = filtrar_items_logica(filtro_dni, filtro_asig, filtro_tipo)

    # 3. Imprimir los resultados
    if resultados:
        print(f"{colores.C_MORADO}\nResultados encontrados ({len(resultados)}):{colores.C_FIN}")
        encabezados = ['id', 'dni', 'nombre', 'asignatura', 'tipo', 'desc', 'nota']
        utilidades.imprimir_tabla(resultados, encabezados)
    else:
        print(f"{colores.C_ROJO}\nNo se encontraron ítems que coincidan con esos criterios de búsqueda.{colores.C_FIN}")


def _gestionar_informes_medias():
    """Función auxiliar (submenú) para gestionar los cálculos de medias."""
    
    opcion_media = -1
    
    # Bucle de submenú (controlado por variable, sin break)
    while opcion_media != 0:
        print(f"{colores.C_MORADO}\n--- Submenú de Medias ---")
        print("1. Ver media por Alumno y Asignatura")
        print("2. Ver media General por Asignatura")
        print(f"0. Volver al menú de Informes{colores.C_FIN}")

        opcion_media = utilidades.pedir_entero_obligatorio(f"{colores.C_MORADO}Selecciona un cálculo: {colores.C_FIN}")

        if opcion_media == 1:
            # --- Lógica de tu Opción A (Por DNI y Asignatura) ---
            print(f"{colores.C_MORADO}\n-- Media por Alumno/Asignatura --{colores.C_FIN}")
            dni = utilidades.pedir_cadena_no_vacia(f"{colores.C_MORADO}DNI del Alumno: {colores.C_FIN}")
            asig = utilidades.pedir_cadena_no_vacia(f"{colores.C_MORADO}Asignatura: {colores.C_FIN}")

            if dni is not None and asig is not None:
                media = calcular_media_alumno_asignatura(dni, asig)
                if media is not None:
                    print(f"{colores.C_MORADO}\nLa media de '{dni}' en '{asig.capitalize()}' es: {media:.2f}{colores.C_FIN}")
                else:
                    print(f"{colores.C_ROJO}\nNo se encontraron notas para '{dni}' en '{asig}'.{colores.C_FIN}")
            else:
                print(f"{colores.C_AMARILLO}Operación cancelada (DNI o Asignatura vacíos).{colores.C_FIN}")

        elif opcion_media == 2:
            # --- Lógica de tu Opción B (General por Asignatura) ---
            print(f"{colores.C_MORADO}\n-- Media General por Asignatura --{colores.C_FIN}")
            asig = utilidades.pedir_cadena_no_vacia(f"{colores.C_MORADO}Asignatura: {colores.C_FIN}")

            if asig is not None:
                media = calcular_media_general_asignatura(asig)
                if media is not None:
                    print(f"{colores.C_MORADO}\nLa media general de '{asig.capitalize()}' es: {media:.2f}{colores.C_FIN}")
                else:
                    print(f"{colores.C_ROJO}\nNo se encontraron notas para '{asig}'.{colores.C_FIN}")
            else:
                print(f"{colores.C_AMARILLO}Operación cancelada.{colores.C_FIN}")

        elif opcion_media == 0:
            print(f"{colores.C_MORADO}\nVolviendo al menú de Informes...{colores.C_FIN}")

        else:
            print(f"{colores.C_ROJO} Opción no válida.{colores.C_FIN}")

def gestionar_informes():
    """
    Muestra las estadísticas agregadas y otros cálculos (tu visión).
    """
    print(f"{colores.C_MORADO}\n--- INFORMES Y ESTADÍSTICAS ---{colores.C_FIN}")

    # 1. Estadística Agregada (Tabla de conteo)
    print(f"{colores.C_MORADO}\nConteo de Tareas y Exámenes por Asignatura:{colores.C_FIN}")
    datos_informe = obtener_estadistica_agregada_asignaturas()
    encabezados_informe = ['Asignatura', 'Tareas', 'Exámenes']
    utilidades.imprimir_tabla(datos_informe, encabezados_informe)
    
    # 2. Cálculo de Medias (Tu submenú) 
    _gestionar_informes_medias()

    # 3. Cálculo Mejor/Peor Asignatura (Max/Min de Medias)
    print(f"{colores.C_MORADO}\n--- Ranking de Asignaturas (Según Media General) ---{colores.C_FIN}")
    ranking = obtener_mejor_peor_asignatura()
    
    if ranking is not None:
        mejor_asig, mejor_media = ranking['mejor']
        peor_asig, peor_media = ranking['peor']

        print(f"{colores.C_VERDE}Mejor Asignatura: {mejor_asig.capitalize()} (Media: {mejor_media:.2f}){colores.C_FIN}")
        print(f"{colores.C_MAGENTA}Peor Asignatura: {peor_asig.capitalize()} (Media: {peor_media:.2f}){colores.C_FIN}")
    else:
        print(f"{colores.C_AMARILLO}\nNo hay suficientes datos de notas para calcular un ranking.{colores.C_FIN}")

def gestionar_menu_guardar_cargar():
    """
    Función auxiliar (submenú) para gestionar las opciones de Guardar/Cargar.
    """
    opcion = -1
    
    # Bucle de submenú (controlado por variable, sin break)
    while opcion != 0:
        print(f"{colores.C_MORADO}\n--- Persistencia de Datos ---{colores.C_FIN}")
        print("1. Guardar datos actuales")
        print("2. Sobreescribir datos del archivo (se perderán los datos en memoria)")
        print("0. Volver al menú principal")

        opcion = utilidades.pedir_entero_obligatorio(f"Selecciona una opción: {colores.C_FIN}")

        if opcion == 1:
            gestionar_guardar()
        elif opcion == 2:
            gestionar_cargar()
        elif opcion == 0:
            print(f"{colores.C_AMARILLO}Volviendo al menú principal...{colores.C_FIN}")
        else:
            print(f"{colores.C_ROJO}Opción no válida.{colores.C_FIN}")


def gestionar_guardar():
    """
    Orquesta el proceso de guardado de datos.
    """
    print(f"{colores.C_MORADO}\n--- GUARDAR DATOS ---{colores.C_FIN}")
    if DATOS_AGENDA:
        if guardar_datos_logica():
            print(f"{colores.C_VERDE} Datos guardados con éxito en '{NOMBRE_ARCHIVO_DATOS}'.{colores.C_FIN}")
        else:
            print(f"{colores.C_ROJO} No se pudieron guardar los datos. Revisa la consola para errores.{colores.C_FIN}")
    else:
        print(f"{colores.C_AMARILLO} No hay datos para guardar.{colores.C_FIN}")

        
def gestionar_cargar():
    """
    Orquesta el proceso de carga de datos.
    """
    print(f"{colores.C_MORADO}\n--- SOBREESCRIBIR DATOS ---{colores.C_FIN}")
    if DATOS_AGENDA:
        # Advertencia al usuario si va a sobrescribir
        confirmacion = utilidades.pedir_cadena_no_vacia(f"{colores.C_AMARILLO}ATENCIÓN: Al cargar, se perderán los datos actuales en memoria. ¿Continuar? (S/N):  {colores.C_FIN}")
        if confirmacion is None or confirmacion.upper() != 'S':
            print(f"{colores.C_AMARILLO} Carga de datos cancelada.{colores.C_FIN}")
            return

    if cargar_datos_logica():
        print(f"{colores.C_VERDE} Datos cargados con éxito desde '{NOMBRE_ARCHIVO_DATOS}'.{colores.C_FIN}")
    else:
        # Si el archivo no existe, la lógica pura devuelve False
        print(f"{colores.C_ROJO} No se encontró el archivo '{NOMBRE_ARCHIVO_DATOS}' o la carga falló. Se inicia con datos vacíos.{colores.C_FIN}")