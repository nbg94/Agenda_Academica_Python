
import utilidades
import servicios
import colores
import persistencia
import controlador

# MAIN 

# =================================================================
# Bucle Principal de Ejecución (Orquestación)
# =================================================================



def controlador_menu():
    """
    Función principal que ejecuta el bucle del menú.
    La condición de salida es 'opcion_valida == 0'.
    """
    opcion_seleccionada = None

    controlador.iniciar_carga_automatica() # Carga automática del json al iniciar
    
    # Bucle del menú principal
    while opcion_seleccionada != 0: 
        mostrar_menu()
        
        # Usamos pedir_entero_obligatorio para forzar la selección de una opción
        opcion = utilidades.pedir_entero_obligatorio("Selecciona una opción: ")

        if opcion == 1:
            controlador.gestionar_alta()
        elif opcion == 2:
            controlador.gestionar_listado()
        elif opcion == 3:
            controlador.gestionar_filtrado_busqueda()
        elif opcion == 4:
            controlador.gestionar_editar_puntuacion()
        elif opcion == 5:
            controlador.gestionar_eliminacion()
        elif opcion == 6:
            controlador.gestionar_informes()
        elif opcion == 7:
            controlador.gestionar_menu_guardar_cargar()
        elif opcion == 0:
            print(f"{colores.C_MAGENTA}\n¡Gracias por usar la Agenda Académica! Cerrando aplicación.{colores.C_FIN}")
            controlador.gestionar_guardar()# Final auto-guardado al salir
            opcion_seleccionada = 0 # Asignación 0 para terminar el bucle
        else:
            print(f"{colores.C_ROJO}Opción no válida. Por favor, elige un número del 0 al 7.{colores.C_FIN}")


def mostrar_menu():
    """Menú principal de la Agenda Académica."""
    print(f"{colores.C_MORADO}\n" + "=" * 50)
    print("---------- AGENDA ACADÉMICA  ----------")
    print("=" * 50)
    print("1) Alta de Tarea/Examen")
    print("2) Listado Completo")
    print("3) Buscar / Filtrar ítems")
    print("4) Editar Puntuación")
    print("5) Eliminar Ítem")
    print("6) Informes y Estadísticas")
    print("7) Guardar / Cargar Datos")
    print("0) Salir")
    print("-" * 50 + f"{colores.C_FIN}")

# =================================================================
#                               MAIN 
# =================================================================
def main():
    """Función principal de ejecución del programa."""
    controlador_menu()

if __name__ == '__main__':
    main()