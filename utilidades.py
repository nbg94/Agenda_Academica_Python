from datetime import datetime
import re
import colores

"""Módulo encargado de la Entrada/Salida y validaciones de los datos introducidos por el usuario"""

# 1. Funciones de ENTRADA (Input) y VALIDACIÓN

def pedir_entero_opcional(mensaje: str) -> int | None:
    """
    Solicita un entero al usuario. Permite entrada vacía (ENTER) para 
    cancelar la operación actual, retornando None.
    
    :param mensaje: El texto a mostrar al usuario.
    :return: El número entero introducido o None si la entrada está vacía.
    """
    valor_valido = False
    resultado = None
    
    while not valor_valido:
        try:
            entrada = input(mensaje).strip()
            
            # Comportamiento Opcional: Retorna None si la entrada está vacía
            if not entrada:
                valor_valido = True
                resultado = None
            else:
                # Conversión
                resultado = int(entrada)
                valor_valido = True
                
        except ValueError:
            print(f"{colores.C_ROJO}Por favor, introduce un número entero válido.{colores.C_FIN}")

    return resultado


def pedir_entero_obligatorio(mensaje: str) -> int:
    """
    Solicita un entero al usuario y OBLIGA a introducir un número válido. 
    No permite entrada vacía (ENTER).
    
    :param mensaje: El texto a mostrar al usuario.
    :return: El número entero introducido.
    """
    valor_valido = False
    resultado = None
    
    while not valor_valido:
        try:
            entrada = input(mensaje).strip()
            
            # Validación: No vacío (Comportamiento Obligatorio)
            if not entrada:
                print(f"{colores.C_ROJO}Error: Este campo no puede estar vacío. Introduce un número.{colores.C_FIN}")
            else:
                # Conversión
                resultado = int(entrada)
                valor_valido = True
                
        except ValueError:
            print(f"{colores.C_ROJO}Error: Por favor, introduce un número entero válido.{colores.C_FIN}")
            # valor_valido sigue siendo False, el bucle se repite

    return resultado


def pedir_cadena_no_vacia(mensaje: str) -> str | None:
    """
    Solicita una cadena de texto y asegura que no esté vacía después de limpiar espacios.
    
    :param mensaje: El texto a mostrar al usuario.
    :return: La cadena de texto validada o None si la entrada está vacía.
    """
    valor_valido = False
    resultado = None
    
    while not valor_valido:
        cadena = input(mensaje).strip()
        
        # Permite entrada vacía para cancelar
        if not cadena:
            valor_valido = True
            resultado = None        
        # Requisito: Validación de no vacío
        else:
            resultado = cadena
            valor_valido = True

    return resultado

def pedir_flotante_simple(mensaje: str) -> float | None:
    """
    Solicita un número decimal (float) al usuario.
    Permite entrada vacía (ENTER) para cancelar la operación, retornando None.
    
    :param mensaje: El texto a mostrar al usuario.
    :return: El número flotante introducido o None si la entrada está vacía.
    """
    valor_valido = False
    resultado = None
    
    while not valor_valido:
        entrada_str = input(mensaje).strip()
        
        if not entrada_str:
            # Entrada vacía, se asume cancelación
            valor_valido = True
            resultado = None
        else:
            try:
                # Conversión a float (double)
                resultado = float(entrada_str)
                valor_valido = True
            except ValueError:
                # Requisito: Manejar errores sin terminar el programa abruptamente
                print(f"{colores.C_ROJO}Error: Por favor, introduce un número decimal válido.{colores.C_FIN}")

    return resultado


def pedir_flotante_en_rango(mensaje: str, min_val: float, max_val: float) -> float | None:
    """
    Solicita un número flotante y valida que esté en el rango [min_val, max_val].
    
    :param mensaje: El texto a mostrar.
    :param min_val: Valor mínimo permitido (inclusivo).
    :param max_val: Valor máximo permitido (inclusivo).
    :return: El número flotante válido o None si la entrada está vacía.
    """
    valor_valido = False
    resultado = None
    
    while not valor_valido:
        entrada_str = input(mensaje).strip()
        
        if not entrada_str:
            valor_valido = True
            resultado = None
        else:
            try:
                valor = float(entrada_str)
                
                if min_val <= valor <= max_val:
                    resultado = valor
                    valor_valido = True
                else:
                    print(f"{colores.C_ROJO}Error: El valor debe estar entre {min_val} y {max_val}.{colores.C_FIN}")
            except ValueError:
                # Requisito: Manejar errores sin terminar el programa abruptamente
                print(f"{colores.C_ROJO}Error: Por favor, introduce un número decimal válido.{colores.C_FIN}")

    return resultado

def pedir_fecha(mensaje: str, formato: str = '%Y-%m-%d') -> str | None:
    """
    Solicita una fecha y valida su formato simple (por defecto AAAA-MM-DD).
    
    :param mensaje: El texto a mostrar.
    :param formato: El formato de fecha esperado (p. ej., '%Y-%m-%d').
    :return: La fecha válida en formato cadena o None si la entrada está vacía.
    """
    valor_valido = False
    resultado = None
    
    while not valor_valido:
        fecha_str = input(mensaje).strip()
        
        if not fecha_str:
            valor_valido = True
            resultado = None
        else:
            try:
                # Requisito: Validaciones de formato simple
                datetime.strptime(fecha_str, formato)
                resultado = fecha_str
                valor_valido = True
            except ValueError:
                formato_ejemplo = formato.replace('%Y', 'AAAA').replace('%m', 'MM').replace('%d', 'DD')
                print(f"{colores.C_ROJO}Error: Formato de fecha incorrecto. Use el formato {formato_ejemplo}.{colores.C_FIN}")

    return resultado

def pedir_cadena_con_patron(mensaje: str, patron_regex: str, msj_error: str) -> str | None:
    """
    Solicita una cadena y valida que cumpla con un patrón de expresión regular.
    Permite entrada vacía (ENTER) para cancelar, retornando None.
    
    :param mensaje: El texto a mostrar al usuario.
    :param patron_regex: El patrón de regex (ej. r'^\d{8}[A-Za-z]$').
    :param msj_error: El mensaje de error si el patrón no coincide.
    :return: La cadena validada o None si la entrada está vacía.
    """
    valor_valido = False
    resultado = None
    
    while not valor_valido:
        cadena = input(mensaje).strip()
        
        if not cadena:
            # Opción 1: Cancelar (entrada vacía)
            valor_valido = True
            resultado = None
        else:
            # Opción 2: Validar patrón
            if re.fullmatch(patron_regex, cadena):
                valor_valido = True
                resultado = cadena
            else:
                # Opción 3: Error
                print(f"{colores.C_ROJO}Error: {msj_error}{colores.C_FIN}")
                # valor_valido sigue False, el bucle repite

    return resultado
    

# 2. Funciones de SALIDA (Output)

def imprimir_tabla(datos: list[dict], encabezados: list[str]):
    """
    Imprime una lista de diccionarios en un formato de tabla legible en consola.
    (Requisito: Informes en consola con formato tabular legible [cite: 27])
    
    :param datos: La lista de diccionarios a imprimir.
    :param encabezados: Lista de las claves (columnas) a mostrar.
    """
    if not datos:
        print(f"{colores.C_AMARILLO}No hay datos para mostrar.{colores.C_FIN}")
        return

    # 1. Calcular el ancho máximo para cada columna
    anchos = {h: len(h) for h in encabezados}
    for fila in datos:
        for h in encabezados:
            valor_str = str(fila.get(h, ''))
            anchos[h] = max(anchos[h], len(valor_str))

    # 2. Imprimir la cabecera y separador
    def dibujar_separador():
        linea_sep = "+"
        for h in encabezados:
            linea_sep += "-" * (anchos[h] + 2) + "+"
        print(linea_sep)

    dibujar_separador()
    
    linea_cabecera = "|"
    for h in encabezados:
        ancho = anchos[h] + 2
        linea_cabecera += h.center(ancho) + "|"
    print(linea_cabecera)
    
    dibujar_separador()

    # 3. Imprimir los datos
    for fila in datos:
        linea_datos = "|"
        for h in encabezados:
            ancho = anchos[h] + 2
            valor_str = str(fila.get(h, '')).ljust(ancho - 2)
            linea_datos += " " + valor_str + " |"
        
        print(linea_datos[:-1] + "|") 
        
    dibujar_separador()    