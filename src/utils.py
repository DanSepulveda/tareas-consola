"""
Módulo de utilidades generales (Helpers).

Módulo con funciones de apoyo no ligadas a la lógica de la aplicación,
como generación de ids, manejo de directorios, etc.
"""

import hashlib
import uuid
import webbrowser
from datetime import date
from pathlib import Path

import src.lib.consola as cli
from src.schemas import Campo, EstadoTarea, Menu, Tarea


def abrir_navegador(ruta: str):
    try:
        path = Path(ruta).resolve().as_uri()
        exito = webbrowser.open(path)
        if not exito:
            raise Exception("Error al abrir el navegador")
    except Exception:
        pass


def dias_desde_hoy(fecha: str) -> int:
    """Cantidad de días entre la fecha indicada en formato dd-mm-aaaa y hoy."""
    try:
        fecha_formateada = date.strptime(fecha, "%d-%m-%Y")
        return (fecha_formateada - date.today()).days
    except ValueError as e:
        raise ValueError("Fecha con formato inválido.") from e


def estilar_estado_tarea(estado: EstadoTarea):
    colors = {
        "Finalizada": "green",
        "En proceso": "blue",
        "Pendiente": "yellow",
    }

    return f"[{colors.get(estado)}]{estado}[/]"


def estilar_vigencia_tarea(fecha: str | None, estado: EstadoTarea) -> str:
    if fecha is None:
        return ""

    if estado == "Finalizada":
        return estado

    dias = dias_desde_hoy(fecha)

    if dias < 0:
        return f"[red]Atrasada {abs(dias)} día(s)[/]"
    if dias == 0:
        return "[yellow]Vence hoy[/]"
    if dias < 4:
        return f"[blue]Vence pronto - {dias} día(s)[/]"
    return "[green]Dentro de plazo[/]"


def formatear_form(campos: list[Campo]) -> str:
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


def generar_tabla_tareas(tareas: list[Tarea]):
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
            estilar_vigencia_tarea(t["fecha_vencimiento"], t["estado"]),
            estilar_estado_tarea(t["estado"]),
        ]
        for indice, t in enumerate(tareas, 1)
    ]
    return (columnas, filas)


def opcion_desde_menu(menu: Menu):
    """Imprime en consola un menú y retorna la opción elegida por el usuario."""
    titulo, opciones = menu["titulo"], menu["opciones"]
    cli.print_panel(titulo=titulo, contenido="\n\n".join(opciones))
    opcion = cli.input_entero("Ingrese una opción", min=1, max=len(opciones))
    return opcion
