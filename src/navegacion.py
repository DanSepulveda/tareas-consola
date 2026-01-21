import src.utilidades.consola as cli
from src.vistas import MENU_PRINCIPAL


def menu_principal():
    cli.print_menu(MENU_PRINCIPAL)
    opciones = list(range(1, len(MENU_PRINCIPAL["opciones"]) + 1))
    opcion = cli.input_entero("Ingrese una opción", opciones)

    match opcion:
        case 1:
            print("Agregar tarea")
            pass
        case 2:
            print("Listar tareas")
            pass
        case 3:
            print("Generar reporte")
            pass
        case 4:
            print("Salir")
            return

    menu_principal()
