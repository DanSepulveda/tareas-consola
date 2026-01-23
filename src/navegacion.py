import src.utilidades.consola as cli
from src.schemas import Estado
from src.vistas import MENU_PRINCIPAL


def menu_principal(estado: Estado):
    cli.print_panel(
        titulo=MENU_PRINCIPAL["titulo"],
        contenido="\n\n".join(MENU_PRINCIPAL["opciones"]),
    )
    max = len(MENU_PRINCIPAL["opciones"])
    opcion = cli.input_entero("Ingrese una opción", min=1, max=max)

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

    menu_principal(estado)
