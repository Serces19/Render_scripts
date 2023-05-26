import subprocess
import sys
import time
from PySide2.QtWidgets import *
from PySide2 import QtCore

from master_ui import *



##################################################################################
#Clases de la interfaz
##################################################################################

class MainWindows(MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        #Setear el boton de render
        self.render_in_progress = False
        self.render_button.clicked.connect(self.renderizar)

    def renderizar(self):
        #Si el render esta en progreso no se ejecuta el resto
        if self.render_in_progress:
            return
        
        #setear el la ubicacion del archivo de nuke
        self.nuke_executable = r'"C:\Program Files\Nuke14.0v4\Nuke14.0"'

        self.comando = list()
        execute = 'execute.py'
        
        #Crear una lista con los archivos a renderizar
        for index in range(self.lista.count()):
            item = self.lista.item(index)
            self.script = item.text()
            self.script = '"' + self.script + '"'
            linea = self.nuke_executable + ' -ti '+ self.script +' < ' + execute
            self.comando.append(linea)

        #Se inicia la clase RenderThread para que la interfaz no se pare mientras se renderiza
        self.thread = RenderThread()
        
        #Se conectan las señales y lo que ejecutaran  
        self.thread.progress.connect(self.update_progress)
        self.thread.current_shot.connect(self.update_shot)
        self.thread.finished.connect(self.rendering_finished)

        #Se inicia el metodo que inicia el render y se pasa el argumento
        self.thread.start_rendering(self.comando)

        #Se establece el status como render in progress
        self.render_button.setEnabled(False)  # Deshabilitar el botón de renderizado
        self.render_in_progress = True  # Establecer el indicador de renderizado en progreso
        self.status.setText("Comenzando") #Establece el texto que va debajo de la barra de progreso

    def update_shot(self, current_shot):
        self.script_actual.setText(current_shot)

    #Actualiza la barra de progresso durante el render
    def update_progress(self, progress):
        self.progressBar.setValue(progress)
        self.status.setText("Renderizando")

    #Se activa una vez el render haya terminado
    def rendering_finished(self):
        self.status.setText("Render finalizado")
        self.render_button.setEnabled(True)  # Habilitar el botón de renderizado
        self.render_in_progress = False  # Establecer el indicador de renderizado en progreso en False


##################################################################################


class RenderThread(QtCore.QThread):
    progress = QtCore.Signal(int)
    current_shot = QtCore.Signal(str)
    finished = QtCore.Signal()

    def __init__(self):
        super().__init__()

    def start_rendering(self, instrucciones):
        self.command = instrucciones
        self.start()


    def run(self):
        print(self.command)
        start_time = time.time()
        for comando in self.command:
            count = 0
            with subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                universal_newlines=True) as proceso:
                while True:
                    linea = proceso.stdout.readline()
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
                        print(shot_name)

                    if linea.startswith('Writing'):
                        count = count + 1
                        frame_actual = count
                        porcentaje = (frame_actual / frame_range) *100
                        self.progress.emit(porcentaje)


        # Cuando se llega aqui es por que el proceso de render terminó
        end_time = time.time()
        render_time: end_time - start_time         
        self.finished.emit()


#################################################################################
#ejecutable
#################################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindows()
    window.show()
    sys.exit(app.exec_())

