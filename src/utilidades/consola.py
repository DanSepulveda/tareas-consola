from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.theme import Theme

from src.constantes import Mensajes
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


def input_entero(mensaje: str, opciones: list[int] = []):
    """
    Solicita un n° entero y comprueba que sea válido.

    Args:
        mensaje (str): Texto a mostrar en consola.
        opciones (list[int], opcional): Lista de números válidos.

    Returns:
        int: número ingresado por el usuario
    """
    while True:
        try:
            numero = int(consola.input(f"[input]{mensaje}: [/]"))

            if (bool(opciones) and numero in opciones) or not bool(opciones):
                return numero
            raise Exception()
        except ValueError:
            print_error(Mensajes.NO_INT)
        except:
            opciones_validas = ", ".join(str(i) for i in opciones)
            print_error(f"{Mensajes.INVALID_INT} {opciones_validas}.")


def print_error(mensaje: str):
    """
    Muestra un mensaje de error en consola.

    Args:
        mensaje (str): Texto del mensaje de error.
    """
    consola.print(f"[error]{mensaje}[/]\n")


def print_menu(menu: Menu, ancho=60):
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
