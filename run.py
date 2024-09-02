import os
import sys


def listar_archivos(directorio):
    # Lista todos los archivos en el directorio
    archivos = [f for f in os.listdir(directorio) if os.path.isfile(os.path.join(directorio, f))]
    return archivos


def seleccionar_archivo(archivos):
    # Muestra una lista numerada de los archivos para que el usuario seleccione
    print("Selecciona un archivo para ejecutar:")
    for i, archivo in enumerate(archivos):
        print(f"{i + 1}. {archivo}")

    # Solicita al usuario que seleccione un archivo
    while True:
        try:
            seleccion = int(input("Introduce el número del archivo: ")) - 1
            if seleccion < 0 or seleccion >= len(archivos):
                print("Selección no válida, intenta nuevamente.")
            else:
                return archivos[seleccion]
        except ValueError:
            print("Por favor, introduce un número válido.")


def ejecutar_script(nombre_script,nombre_archivo):
    """ Ejecuta un script de Python pasando el nombre del archivo como argumento"""
    os.system(f"{sys.executable} {nombre_script} {nombre_archivo}")


def seleccionar_script(archivo_seleccionado):
    """Selecciona el script a ejecutar según el tipo de modelo"""
    scripts = {
        "keras": os.path.abspath(os.path.join(__file__,"..","CNN","predict.py")),
        "pkl": os.path.abspath(os.path.join(__file__,"..","SVM","predict.py"))
    }
    termination = archivo_seleccionado.split(".")[-1]
    return scripts[termination]


if __name__ == "__main__":
    # Directorio relativo donde buscar los archivos
    directorio_modelos =os.path.abspath(os.path.join(__file__,"..","models"))

    # Listar archivos en el directorio
    archivos = listar_archivos(directorio_modelos)

    if not archivos:
        raise Exception("No se encontraron archivos en el directorio.")

    archivo = seleccionar_archivo(archivos)
    # Seleccionar un archivo de la lista
    archivo_seleccionado = os.path.join(directorio_modelos,archivo)
    script = seleccionar_script(archivo_seleccionado)

    # Ejecutar el script seleccionado
    ejecutar_script(script,archivo_seleccionado)
