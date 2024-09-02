import os
import subprocess
import sys

def create_virtualenv(venv_name):
    """ Crea un entorno virtual """
    if not os.path.exists(venv_name):
        subprocess.check_call([sys.executable, "-m", "venv", venv_name])

def install_requirements(venv_name):
    """ Instala los paquetes desde requirements.txt en el entorno virtual """
    pip_path = os.path.join(venv_name, "Scripts", "pip.exe")
    os.system(os.path.join(venv_name, "Scripts", "activate"))
    os.system(" ".join([pip_path, "install", "-r", "requirements.txt"]))

def run_script(venv_name, script_name):
    """ Ejecuta el script dentro del entorno virtual """
    python_path = os.path.join(venv_name, "Scripts", "python.exe")
    os.system(" ".join([python_path, script_name]))

if __name__ == "__main__":
    venv_name = "venv"
    script_name = "run.py"

    print("Creating virtual environment")
    create_virtualenv(venv_name)
    print("Installing requirements")
    install_requirements(venv_name)
    print("Running...")
    run_script(venv_name, script_name)
