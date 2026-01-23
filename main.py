import src.repositorio as repo
import src.utilidades.consola as cli
from src.acceso import login
from src.navegacion import menu_principal


def main():
    usuario_logueado = login()

    if not usuario_logueado:
        cli.print_error("No se ha logueado ningún usuario.")
        return

    tareas = repo.obtener_tareas_usuario(usuario_logueado["id"])
    menu_principal(estado={"usuario": usuario_logueado, "tareas": tareas})


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
