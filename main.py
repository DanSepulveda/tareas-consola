import src.utilidades.consola as cli
from src.acceso import login
from src.navegacion import menu_principal


def main():
    usuario_logueado = login()

    if not usuario_logueado:
        cli.print_error("No se ha logueado ningún usuario.")
        return

    menu_principal()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
