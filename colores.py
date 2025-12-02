# Constantes ANSI para colores (Foreground/Texto)
C_FIN = '\033[0m'     # Resetear color
C_NEGRO = '\033[30m'  
C_ROJO = '\033[91m'   # Rojo claro (Error/Alerta)
C_VERDE = '\033[92m'  # Verde claro (Éxito)
C_AMARILLO = '\033[93m' # Amarillo (Advertencia/Info)
C_MORADO = '\033[94m'   # Azul (Títulos/Destacado)
C_MAGENTA = '\033[95m' # Magenta (Opciones/Menus)
C_CYAN = '\033[96m'   # Cyan (Subtítulos)
C_BLANCO = '\033[97m'

# Prefijos comunes para mensajes
PREFIJOS = {
    "EXITO": f"{C_VERDE}{C_FIN}",
    "ERROR": f"{C_ROJO}{C_FIN}",
    "INFO": f"{C_AMARILLO}{C_FIN}",
    "ALERTA": f"{C_ROJO}{C_FIN}"
}