import src.lib.consola as cli
import src.lib.helpers as utils
import src.servicios as servicios
from src.schemas import Campo, Estado, Form, Menu, Tarea


def menu_principal(estado: Estado):
    menu: Menu = {
        "titulo": "🔸 GESTIÓN DE TAREAS 🔸",
        "opciones": [
            "📌 1. Agregar tarea",
            "📋 2. Listar tareas",
            "💾 3. Exportar datos",
            "🚪 4. Cerrar sesión",
        ],
    }

    titulo, opciones = menu["titulo"], menu["opciones"]
    cli.print_panel(titulo=titulo, contenido="\n\n".join(opciones))
    opcion = cli.input_entero("Ingrese una opción", min=1, max=len(opciones))

    match opcion:
        case 1:
            formulario_agregar(estado)
        case 2:
            menu_listar(estado["tareas"])
        case 3:
            print("Generar reporte")
            pass
        case 4:
            cli.print_alerta("Ha cerrado la sesión.")
            return

    menu_principal(estado)


# TODO: agregar regex para validar fecha y otros inputs
# TODO: revisar color de placeholder o label, para que no se confundan
def formulario_agregar(estado: Estado):
    tareas, usuario = estado["tareas"], estado["usuario"]

    formulario: Form = {
        "titulo": "📌 AGREGAR TAREA 📌",
        "campos": [
            {
                "label": "Título",
                "placeholder": "Ej. Terminar proyecto 1",
                "nombre": "titulo",
                "input": cli.input_texto,
            },
            {
                "label": "Categoría(s)",
                "placeholder": "Ej. Urgente, Desarrollo, Proyecto.",
                "nombre": "categoria",
                "input": cli.input_texto,
            },
            {
                "label": "Fecha límite",
                "placeholder": "Ej. 24-02-2026 o vacío",
                "nombre": "fecha_vencimiento",
                "input": cli.input_texto,
            },
        ],
    }

    titulo, campos = formulario["titulo"], formulario["campos"]
    cli.print_panel(titulo=titulo, contenido=formatear_contenido(campos))

    for indice, campo in enumerate(campos):
        valor = campo["input"](f"Ingrese {campo['label']}")
        campos[indice]["valor"] = valor
        cli.print_panel(titulo=titulo, contenido=formatear_contenido(campos))

    nueva_tarea = {c["nombre"]: c.get("valor") for c in campos}
    servicios.crear_tarea(tareas, nueva_tarea, usuario)

    cli.print_exito("Tarea agregada correctamente 🎉")
    cli.input_continuar("volver al menú principal")


def menu_listar(tareas: list[Tarea]):
    if not tareas:
        cli.print_panel(
            titulo="MIS TAREAS",
            contenido="👻 No hay tareas registradas 👻".center(48),
        )
        cli.input_continuar("volver al menú principal")
        return

    menu: Menu = {
        "titulo": "📋 LISTAR TAREAS 📋",
        "opciones": [
            "🟢 1. Ver en consola",
            "🟢 2. Ver en navegador",
            "🟠 3. Volver al menú principal",
        ],
    }

    titulo, opciones = menu["titulo"], menu["opciones"]
    cli.print_panel(titulo=titulo, contenido="\n\n".join(opciones))
    opcion = cli.input_entero("Ingrese una opción", min=1, max=len(opciones))

    match opcion:
        case 1:
            ver_en_consola(tareas)
        case 2:
            ver_en_navegador(tareas)
        case 3:
            return

    menu_listar(tareas)


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


def formatear_contenido(campos: list[Campo]) -> str:
    return "\n\n".join(
        [
            f"👉 {c['label']}: [dim not bold]{c['placeholder']}[/]"
            if c.get("valor") is None
            else f"👉 {c['label']}: [green not bold]{c.get('valor')}[/]"
            for c in campos
        ]
    )
