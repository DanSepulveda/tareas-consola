"""
Interfaz de interacción por consola (CLI).

Centralización de todas las funciones de entrada y salida de datos.
Proporciona métodos para mostrar alertas, errores y solicitar datos validados,
asegurando una UI consistente en toda la aplicación.
"""

from datetime import date

from rich import box
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme


ANCHO = 60
PADDING = 4


tema = Theme(
    {
        "ok": "green",
        "error": "red",
        "input": "blue",
        "alerta": "yellow",
        "info": "yellow",
    }
)

consola = Console(theme=tema)


def input_confirmar(mensaje: str) -> bool:
    """Solicita y valida una respuesta booleana (s/n)."""
    while True:
        respuesta = consola.input(f"[input]{mensaje} (s/n):[/] ").lower()

        if respuesta in ["s", "n"]:
            return respuesta == "s"
        print_error("Opción inválida. Ingrese 's' o 'n'")


def input_continuar(mensaje: str) -> None:
    """Simula una pausa. Usuario debe presionar ENTER para continuar."""
    consola.input(
        f"[plum1]Presione [bold]ENTER[/bold] para {mensaje}...[/plum1] "
    )


def input_entero(
    mensaje: str, min: int | None = None, max: int | None = None
) -> int:
    """Solicita y valida un número entero (opcionalmente se puede especificar min y max)"""
    if min is not None and max is not None and min > max:
        raise ValueError(f"min ({min}) no puede ser mayor a max ({max})")

    while True:
        try:
            numero = int(consola.input(f"[input]{mensaje}:[/] "))

            if (
                min is not None
                and max is not None
                and (numero < min or numero > max)
            ):
                raise ValueError(f"El número debe estar entre {min} y {max}.")

            if min is not None and numero < min:
                raise ValueError(
                    f"El número debe ser mayor o igual que {min}."
                )

            if max is not None and numero > max:
                raise ValueError(
                    f"El número debe ser menor o igual que {max}."
                )

            return numero
        except ValueError as e:
            error = (
                str(e)
                if "invalid literal" not in str(e)
                else "Debe ingresar un número entero."
            )
            print_error(error)


def input_fecha(mensaje: str, permitir_vacio: bool = True):
    """Solicita y valida una fecha con formato dd-mm-aaaa"""
    while True:
        fecha = consola.input(f"[input]{mensaje}:[/] ")
        if fecha == "" and permitir_vacio:
            return "-"

        try:
            date.strptime(fecha, "%d-%m-%Y")
            return fecha
        except ValueError as e:
            error = "Formato de fecha inválido"
            if "must be in range" in str(e):
                dias = str(e).split("..")[1][:2]
                error = f"Fecha inválida. El mes ingresado tiene {dias} días"
            print_error(error)


def input_texto(mensaje: str, min_len: int = 1, max_len: int = 50) -> str:
    """Solicita texto y valida que su longitud esté en el rango indicado."""
    if min_len > max_len:
        raise ValueError(
            f"min_len ({min_len}) no puede ser mayor a max_len ({max_len})"
        )

    while True:
        texto = consola.input(f"[input]{mensaje}:[/] ")

        if len(texto) <= max_len and len(texto) >= min_len:
            return texto
        print_error(f"Debe contener entre {min_len} y {max_len} caracteres.")


def print_alerta(mensaje: str) -> None:
    consola.print(f"[alerta]{mensaje}[/]\n")


def print_error(mensaje: str) -> None:
    consola.print(f"[error]{mensaje}[/]\n")


def print_exito(mensaje: str) -> None:
    consola.print(f"[ok]{mensaje}[/]\n")


def print_panel(
    titulo: str,
    contenido: str,
    subtitulo: str = "",
    centrar: bool = True,
    limpiar: bool = True,
) -> None:
    """Imprime un Panel en consola (Contenedor con bordes)"""
    contenido = contenido.center(ANCHO - PADDING * 3) if centrar else contenido
    consola.print(
        "\n" * 60 if limpiar else "",
        Panel(
            Padding(f"[bold bright_white]{contenido}[/]", (1, PADDING)),
            title=f"[bold blue_violet]{titulo}[/]",
            border_style="light_steel_blue",
            subtitle=subtitulo,
            width=ANCHO,
        ),
        "",
    )


def print_tabla(
    titulo: str,
    columnas: list[str],
    filas: list[list[str]],
    caption: str | None = None,
) -> None:
    """Imprime una tabla en consola."""
    tabla = Table(
        title=titulo,
        box=box.HORIZONTALS,
        show_lines=True,
        border_style="dim",
        title_style="bold blue_violet",
        header_style="bright_white bold",
        caption=caption,
    )

    for columna in columnas:
        tabla.add_column(columna)

    for fila in filas:
        tabla.add_row(*fila)

    consola.print("\n" * 60, tabla, "")


def print_toast(mensaje_toast: str, mensaje_pausa: str = "continuar"):
    """Imprime un Panel en consola y agrega una pausa."""
    tipo, mensaje = mensaje_toast.split(":")

    consola.print(
        "",
        Panel(
            mensaje.center(ANCHO - 4),
            title=tipo.replace("info", "información").upper(),
            border_style=tipo,
            width=ANCHO,
        ),
    )
    input_continuar(mensaje_pausa)
