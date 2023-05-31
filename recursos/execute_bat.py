import subprocess
import sys
import re

# Comandos a ejecutar
comandos = [
    r'"C:\Program Files\Nuke14.0v4\Nuke14.0" -xi -V 2 C:/Users/sergi/Desktop/pruebas/pruebas.nk',
    r'"C:\Program Files\Nuke14.0v4\Nuke14.0" -xi -V 2 C:/Users/sergi/Desktop/pruebas/pruebas_2.nk',
    r'"C:\Program Files\Nuke14.0v4\Nuke14.0" -xi -V 2 C:/Users/sergi/Desktop/pruebas/pruebas_3.nk'
]

# Ejecutar los comandos en secuencia
for comando in comandos:

    with subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) as proceso:
        
        linea = proceso.stdout.readline()
        print(linea)
        # linea = proceso.stdout.readline()
        # Leer la salida y los errores del proceso
        salida, error = proceso.communicate()

        # Obtener el código de salida
        codigo_salida = proceso.returncode

        # Imprimir la salida, el error y el código de salida
        print("Salida:", salida)
        print("Error:", error)
        print("Código de salida:", codigo_salida)

