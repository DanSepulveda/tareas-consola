"""
Módulo de utilidades generales (Helpers).

Módulo con funciones de apoyo para generar ids, obtener hash de clave,
realizar ciertas operaciones, y dar formato a algunas salidas de texto.
"""

import hashlib
import uuid
import webbrowser
from datetime import date
from pathlib import Path

import src.lib.consola as cli
from src.definiciones.schemas import Campo, EstadoTarea, Menu, Tarea


def abrir_navegador(ruta: str):
    """Abre el navegador web en la ruta indicada."""
    try:
        path = Path(ruta).resolve().as_uri()
        exito = webbrowser.open(path)
        if not exito:
            cli.print_error("Error al abrir el navegador")
    except Exception as e:
        raise Exception("Error al abrir navegador.") from e


def dias_desde_hoy(fecha: str) -> int:
    """Cantidad de días entre la fecha indicada en formato dd-mm-aaaa y hoy."""
    try:
        fecha_formateada = date.strptime(fecha, "%d-%m-%Y")
        return (fecha_formateada - date.today()).days
    except ValueError as e:
        raise ValueError("Fecha con formato inválido.") from e


def estilar_estado_tarea(estado: EstadoTarea):
    """Agrega color al estado de la tarea para identificarlas fácilmente."""
    colors = {
        "Finalizada": "green",
        "En proceso": "blue",
        "Pendiente": "yellow",
    }
    return f"[{colors[estado]}]{estado}[/]"


def estilar_vigencia_tarea(fecha: str | None, estado: EstadoTarea) -> str:
    """Genera un texto en color para identificar la fecha límite de una tarea."""
    if fecha is None or estado == "Finalizada":
        return ""

    dias = dias_desde_hoy(fecha)
    palabra = "día" if abs(dias) == 1 else "días"

    if dias < 0:
        return f"[red]Atrasada ({abs(dias)} {palabra})[/]"
    if dias == 0:
        return "[yellow]Vence hoy[/]"
    if dias < 4:
        return f"[blue]Vence pronto ({dias} {palabra})[/]"
    return f"[green]A tiempo ({dias} {palabra})[/]"


def formatear_form(campos: list[Campo]) -> str:
    """
    Formatea los datos mostrados por un formulario. Si los campos no tienen
    calor, se muestra el Label + el Placeholder. A medida que se solicitan los
    datos, el placeholder se reemplaza por el texto ingresado por el usuario.
    """
    return "\n\n".join(
        [
            f"👉 {c['label']}: [dim not bold]{c['placeholder']}[/]"
            if c.get("valor") is None
            else f"👉 {c['label']}: [green not bold]{c.get('valor')}[/]"
            for c in campos
        ]
    )


def generar_hash(clave: str) -> str:
    """Genera un hash para la clave del usuario."""
    return hashlib.sha256(clave.encode("utf-8")).hexdigest()


def generar_id() -> str:
    """Genera un identificador único."""
    return str(uuid.uuid4())


def generar_datos_tabla(
    tareas: list[Tarea], destacar_finalizadas: bool = False
):
    """
    Genera las filas y columnas para mostrar las tareas en una tabla.
    Opcionalmente se pueden destacar las tareas finalizadas.
    """
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
            f"[white on red]{t['titulo']}[]"
            if destacar_finalizadas and t["estado"] == "Finalizada"
            else t["titulo"],
            t["categoria"],
            t["fecha_creacion"],
            t["fecha_vencimiento"],
            estilar_vigencia_tarea(t["fecha_vencimiento"], t["estado"]),
            estilar_estado_tarea(t["estado"]),
        ]
        for indice, t in enumerate(tareas, 1)
    ]
    return (columnas, filas)


def obtener_opcion_menu(menu: Menu):
    """
    Imprime en consola un menú, solicita una opción al usuario y
    retorna la opción, previamente validada.
    """
    titulo, opciones = menu["titulo"], menu["opciones"]
    cli.print_panel(titulo=titulo, contenido="\n\n".join(opciones))
    opcion = cli.input_entero("Ingrese una opción", min=1, max=len(opciones))
    return opcion
