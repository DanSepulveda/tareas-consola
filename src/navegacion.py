import src.lib.consola as cli
import src.servicios as servicios
import src.utils as utils
from src.schemas import Estado, Form, Menu, Tarea


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

    opcion = utils.opcion_desde_menu(menu)

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
    cli.print_panel(titulo=titulo, contenido=utils.formatear_form(campos))

    for indice, campo in enumerate(campos):
        valor = campo["input"](f"Ingrese {campo['label']}")
        campos[indice]["valor"] = valor
        cli.print_panel(titulo=titulo, contenido=utils.formatear_form(campos))

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

    opcion = utils.opcion_desde_menu(menu)

    match opcion:
        case 1:
            columnas, filas = utils.generar_tabla_tareas(tareas)
            cli.print_table("Lista de tareas", columnas, filas)
            cli.input_continuar("volver al menú")
        case 2:
            print("Ver en navegador")
        case 3:
            return

    menu_listar(tareas)
