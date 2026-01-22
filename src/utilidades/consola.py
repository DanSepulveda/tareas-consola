from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.theme import Theme

from src.schemas import Menu


tema = Theme(
    {
        "ok": "green",
        "error": "red",
        "input": "blue",
        "alerta": "yellow",
        "info": "white",
    }
)

consola = Console(theme=tema)


def input_confirmar(mensaje: str) -> bool:
    """
    Solicita una confirmación al usuario (opción booleana s/n).

    Args:
        mensaje (str): Texto a mostrar en consola.

    Returns:
        bool: True en caso de confirmar. False en caso contrario
    """
    while True:
        respuesta = consola.input(f"[alerta]{mensaje} (s/n): [/]").lower()

        if respuesta in ["s", "n"]:
            return respuesta == "s"
        print_error("Opción inválida. Ingrese 's' o 'n'")


def input_entero(mensaje: str, min: int | None = None, max: int | None = None) -> int:
    """
    Solicita y comprueba que lo ingresado por el usuario sea un número entero.
    Si se señala "min" y/o "max", se verifica que cumpla con esas condiciones.

    Args:
        mensaje (str): Texto a mostrar en consola.
        min (int, opcional): Valor mínimo (incluído)
        max (int, opcional): Valor máximo (incluído)

    Returns:
        int: Número ingresado por el usuario.
    """
    if min is not None and max is not None and min > max:
        raise ValueError(f"min ({min}) no puede ser mayor a max ({max})")

    while True:
        try:
            numero = int(consola.input(f"[input]{mensaje}: [/]"))

            if min is not None and max is not None and (numero < min or numero > max):
                raise ValueError(f"El número debe estar entre {min} y {max}.")

            if min is not None and numero < min:
                raise ValueError(f"El número debe ser mayor o igual que {min}.")

            if max is not None and numero > max:
                raise ValueError(f"El número debe ser menor o igual que {max}.")

            return numero
        except ValueError as e:
            error = (
                str(e)
                if "invalid literal" not in str(e)
                else "Debe ingresar un número entero."
            )
            print_error(error)


def input_texto(mensaje: str, min_len: int = 1, max_len: int = 50) -> str:
    """
    Solicita texto al usuario y verifica que su longitud esté en el rango indicado.

    Args:
        min_len (int, opcional): Cantidad mínima de caracteres.
        max_len (int, opcional): Cantidad máxima de caracteres.

    Returns:
        str: Texto ingresado por el usuario.
    """
    if min_len > max_len:
        raise ValueError(f"min_len ({min}) no puede ser mayor a max_len ({max})")

    while True:
        texto = consola.input(f"[input]{mensaje}: [/]")

        if len(texto) <= max_len and len(texto) >= min_len:
            return texto
        print_error(f"El texto debe contener entre {min} y {max} caracteres.")


def print_error(mensaje: str) -> None:
    """
    Muestra un mensaje de error en consola.

    Args:
        mensaje (str): Texto del mensaje de error.
    """
    consola.print(f"[error]{mensaje}[/]\n")


def print_menu(menu: Menu, ancho=60) -> None:
    """
    Muestra un menú de opciones en consola.

    Args:
        menu (Menu): Menú de navegación.
        ancho (int, opcional): Ancho del menú en consola.
    """
    titulo, opciones = menu["titulo"], menu["opciones"]
    contenido = "\n"

    for opcion in opciones:
        contenido += f"{opcion}\n\n"

    panel = Panel(
        Padding(contenido[:-1], (0, 0, 0, 3)),
        title=f"[bold cyan]{titulo}[/bold cyan]",
        border_style="cyan",
        width=ancho,
    )
    consola.print(panel)
