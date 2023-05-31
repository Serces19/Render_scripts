import subprocess
import os
import sys
import time
import re
from PySide2.QtMultimedia import QSoundEffect
from PySide2.QtWidgets import *
from PySide2 import QtCore
from PySide2.QtCore import QTimer, QTime, QUrl
from master_ui import *



##################################################################################
#Clases de la interfaz
##################################################################################

class MainWindows(MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.thread = None
        
        # Setear el boton de render
        self.render_in_progress = False
        self.render_button.clicked.connect(self.renderizar)
        self.button_stop.clicked.connect(self.renderizar)

        # Creamos el objeto QSoundEffect
        self.sound_effect = QSoundEffect()

        # Cargamos un sonido de sistema predeterminado en función del sistema operativo
        if sys.platform.startswith('win'):
            self.sound_effect.setSource(QUrl.fromLocalFile('C:/Windows/Media/Windows Ding.wav'))
        elif sys.platform.startswith('darwin'):
            self.sound_effect.setSource(QUrl.fromLocalFile('/System/Library/Sounds/Ping.aiff'))
        elif sys.platform.startswith('linux'):
            self.sound_effect.setSource(QUrl.fromLocalFile('/usr/share/sounds/freedesktop/stereo/complete.oga'))

    def renderizar(self):
        # Si el render esta en progreso no se ejecuta el resto
        if self.render_in_progress:
            return
        
        # setear el nombre del write
        input_write = self.input_write.text()

        # setear el la ubicacion del archivo de nuke
        self.nuke_executable = self.nuke_dir.text()


        # Si se dejo el campo vacio la opcion por defecto se define:
        if self.nuke_executable == "":
            self.nuke_executable = r'C:\Program Files\Nuke14.0v4\Nuke14.0.exe'

        # Si la ubicacion del archivo de nuke no es real se lanza un mensaje de alerta  
        if not os.path.exists(self.nuke_executable):
            self.show_message_box('La ubicacion de Nuke es incorrecta')
            return
        
        # Se agregan comillas dobles para evitar problemas
        self.nuke_executable = '"' + self.nuke_executable + '"'

        # Inicar la lista que contiene los archivos de nuke a renderizar
        self.comando = list()

        # Definir el codigo de python que se guardara en un archivo temporal
        execute = '''

import nuke

print('Iniciando execute.py')

########################################
# Accede a la raíz del proyecto
root_node = nuke.root()

# Obtén el primer y último fotograma
first_frame = int(root_node['first_frame'].value())
last_frame = int(root_node['last_frame'].value())
frame_range = last_frame - first_frame

print('last frame:', frame_range)

# Obtener el nombre del script
shot_name = nuke.tcl('regsub -all {_v[0-9]+} [file rootname [file tail [value root.name]]] ""')
print('shot name:', shot_name)

######################################
#Renderizar
node_name = "Write1"
if nuke.exists(node_name):
    write_node = nuke.toNode(node_name)
    nuke.render(write_node, continueOnError = True)
else:
    print(f"El nodo {node_name} no existe")


#################
quit()

        '''

        # Modificar el valor de la variable en execute.py
        if not input_write == "":
            execute = execute.replace('node_name = "Write1"', f'node_name = "{input_write}"')

        # Guardar el contenido modificado en un archivo temporal
        execute_temp = 'execute_temp.py'
        with open(execute_temp, 'w') as file:
            file.write(execute)


        #Crear una lista con los archivos a renderizar
        for index in range(self.lista.count()):
            item = self.lista.item(index)
            self.script = item.text()
            self.script = '"' + self.script + '"'
            linea = self.nuke_executable + ' -ti -V2 '+ self.script +' < ' + execute_temp
            self.comando.append(linea)

        #Se inicia la clase RenderThread para que la interfaz no se pare mientras se renderiza
        self.thread = RenderThread()
        
        #Se conectan las señales y lo que ejecutaran  
        self.thread.progress.connect(self.update_progress)
        self.thread.descripcion.connect(self.update_descripcion)
        self.thread.current_shot.connect(self.update_shot)
        self.thread.finished.connect(self.rendering_finished)
        self.thread.tiempo_restante.connect(self.update_rest_time)
        self.thread.not_node.connect(self.not_node)

        #Se inicia el metodo que inicia el render y se pasa como argumentos los comandos a ejecutar
        self.thread.start_rendering(self.comando)

        #Se establece el status como render in progress
        self.render_button.setEnabled(False)  # Deshabilitar el botón de renderizado
        self.render_in_progress = True  # Establecer el indicador de renderizado en progreso
        self.status.setText("Comenzando") #Establece el texto que va debajo de la barra de progreso
        self.progressBar.setValue(0)

        #comienza a contar los miniutos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Actualiza cada segundo (1000 ms)
        self.start_time = QTime.currentTime()

    def not_node(self):
        self.show_message_box('El nodo no existe')
        return

    def show_message_box(self, mensaje):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle('¡Advertencia!')
        msg_box.setText(mensaje)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    #Actualiza el nombre del archivo de nuke que se esta renderizando
    def update_shot(self, current_shot):
        self.status.setText(f'Renderizando: {current_shot}')

    #Actualiza la barra de progresso durante el render
    def update_progress(self, progress):
        self.progressBar.setValue(progress)

    #Actualiza la descripcion de lo que se esta renderizando
    def update_descripcion(self, descripcion):
        self.descripcion.setText(descripcion)
    
    #Actualiza el tiempo restante de render
    def update_rest_time(self, tiempo_restante):
        tiempo_restante = round(abs(tiempo_restante), 1)
        tiempo_restante = str(tiempo_restante)
        self.tiempo_restante.setText(f'Tiempo restante: {tiempo_restante}')

    #Se activa una vez el render haya terminado
    def rendering_finished(self):
        self.timer.stop()
        self.status.setText("Render finalizado")
        self.render_button.setEnabled(True)  # Habilitar el botón de renderizado
        self.render_in_progress = False  # Establecer el indicador de renderizado en progreso en False
        self.tiempo_restante.setText('-')
        self.play_sound()
    
    # Actualizar tiempo total de render
    def update_time(self):
        current_time = QTime.currentTime()
        elapsed_seconds = self.start_time.secsTo(current_time)
        self.tiempo.setText(f"tiempo de render: {elapsed_seconds}")


    def play_sound(self):
        # Reproducir el sonido
        self.sound_effect.play()
##################################################################################


class RenderThread(QtCore.QThread):
    progress = QtCore.Signal(int)
    tiempo_restante = QtCore.Signal(float)
    current_shot = QtCore.Signal(str)
    descripcion = QtCore.Signal(str)
    finished = QtCore.Signal()
    tiempo = QtCore.Signal(int)
    not_node = QtCore.Signal()

    def __init__(self):
        super().__init__()

    def start_rendering(self, instrucciones):
        self.command = instrucciones
        self.start()

    def run(self):
        print(self.command)
        self.start_time = time.time()
        for comando in self.command:
            count = 0
            with subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                universal_newlines=True) as self.proceso:
                while True:
                    linea = self.proceso.stdout.readline()
                    print(linea)
                    if not linea:
                        print('linea not')
                        break
                    if 'last frame:' in linea:
                        frame_range = linea.split()
                        frame_range = frame_range[-1]
                        frame_range = int(frame_range)

                    if 'shot name:' in linea:
                        shot_name = linea.split()
                        shot_name = shot_name[-1]
                        shot_name = str(shot_name)
                        self.current_shot.emit(shot_name)

                    if 'Writing ' in linea:
                        count = count + 1
                        frame_actual = count/2
                        porcentaje = (frame_actual / frame_range) *100
                        porcentaje = int(porcentaje)
                        self.progress.emit(porcentaje)
                        
                        end_time = time.time()
                        frames_restantes = frame_range - frame_actual
                        tiempo = end_time - self.start_time
                        time_per_frame = tiempo/frame_actual
                        tiempo_restante = time_per_frame * frames_restantes
                        self.tiempo_restante.emit(tiempo_restante)

                        actual = linea.split()
                        actual = actual[0:-3]
                        actual = ' '.join(actual)
                        self.descripcion.emit(actual)

                    if linea.startswith('Total render time:'):
                        self.descripcion.emit(linea)
                    
                    if 'no existe' in linea:
                        # Se utiliza regex para extraer la informacion del nodo que no existe
                        patron = r"(El nodo.*)"
                        nombre_del_nodo = re.search(patron, linea)

                        if nombre_del_nodo:
                            nombre_del_nodo = nombre_del_nodo.group(1).strip()
                        
                        # Enviamos la informacion y las señales
                        self.descripcion.emit(nombre_del_nodo)
                        self.not_node.emit()
                        

                    end_time = time.time()
                    tiempo = end_time - self.start_time
                    tiempo = int(tiempo)
                    self.tiempo.emit(tiempo)
                    
        # Cuando se llega aqui es por que el proceso de render terminó       
        self.finished.emit()

    def stop(self):
        if self.render_thread is not None and self.render_thread.is_alive():
            self.render_thread.stop()
            self.proceso.terminate()
#################################################################################
#ejecutable
#################################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindows()
    window.show()
    sys.exit(app.exec_())

