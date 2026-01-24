import src.utilidades.consola as cli
import src.utilidades.helpers as utils
from src.schemas import Estado, Tarea
from src.vistas import MENU_LISTADO, MENU_PRINCIPAL


def menu_principal(estado: Estado):
    titulo, opciones = MENU_PRINCIPAL["titulo"], MENU_PRINCIPAL["opciones"]
    cli.print_panel(titulo=titulo, contenido="\n\n".join(opciones))
    opcion = cli.input_entero("Ingrese una opción", min=1, max=len(opciones))

    match opcion:
        case 1:
            print("Agregar tarea")
            pass
        case 2:
            listar_tareas(estado["tareas"])
        case 3:
            print("Generar reporte")
            pass
        case 4:
            print("Salir")
            return

    menu_principal(estado)


def listar_tareas(tareas: list[Tarea]):
    if not tareas:
        cli.print_panel(
            titulo="Mis tareas",
            contenido="No hay tareas registradas.".center(48),
        )
        cli.input_continuar("volver al menú")
        return

    titulo, opciones = MENU_LISTADO["titulo"], MENU_LISTADO["opciones"]
    cli.print_panel(titulo=titulo, contenido="\n\n".join(opciones))
    opcion = cli.input_entero("Ingrese una opción", min=1, max=len(opciones))

    match opcion:
        case 1:
            ver_en_consola(tareas)
        case 2:
            ver_en_navegador(tareas)
        case 3:
            return

    listar_tareas(tareas)


def ver_en_consola(tareas: list[Tarea]):
    columnas = [
        "ID",
        "Título",
        "Categoría",
        "Fecha creación",
        "Fecha límite",
        "Vigencia",
        "Estado",
    ]
    filas = [
        [
            str(indice),
            t["titulo"],
            t["categoria"],
            t["fecha_creacion"],
            t["fecha_vencimiento"],
            estilar_vigencia(t["fecha_vencimiento"], t["estado"]),
            estilar_estado(t["estado"]),
        ]
        for indice, t in enumerate(tareas, 1)
    ]

    cli.print_table("Lista de tareas", columnas, filas)
    cli.input_continuar("volver al menú")


def estilar_estado(estado: str):
    if estado == "Finalizada":
        color = "green"
    elif estado == "En proceso":
        color = "blue"
    else:
        color = "yellow"
    return f"[{color}]{estado}[/]"


def estilar_vigencia(fecha: str | None, estado: str) -> str:
    if fecha is None:
        return ""

    if estado == "Finalizada":
        return estado

    dias = utils.dias_desde_hoy(fecha)

    if dias < 0:
        return f"[red]Atrasada {abs(dias)} día(s)[/]"
    if dias == 0:
        return "[yellow]Vence hoy[/]"
    if dias < 4:
        return f"[blue]Vence pronto - {dias} día(s)[/]"
    return "[green]Dentro de plazo[/]"


def ver_en_navegador(tareas: list[Tarea]):
    pass
