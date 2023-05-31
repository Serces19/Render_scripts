import subprocess
import re
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QProgressBar, QPushButton, QLabel, QLineEdit
from PySide2 import QtWidgets, QtCore
from controladores.main_ui import Ui_Nuke_Render
from PySide2.QtWidgets import QListView, QVBoxLayout, QWidget, QAbstractItemView, QListWidgetItem, QListWidget
from PySide2.QtCore import Qt, QMimeData, QUrl



##################################################################################
#Clases de la interfaz
##################################################################################

class MainWindow(QMainWindow, Ui_Nuke_Render):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        #Setear cosas
        self.render_button.clicked.connect(self.renderizar)
        self.render_in_progress = False
        
        # #Crear lista y añadirla al layout
        self.list_widget = FileListWidget(self)
        self.gridLayout.addWidget(self.list_widget)

        

    def renderizar(self):
        #Si el render esta en progreso no se ejecuta el resto

        if self.render_in_progress:
            return
        
        #setear el nombre del write que debera ser el mismo para todos los scripts
        self.write = self.input_write.text()
        count = 0
        union = ' && '
        for index in range(self.list_widget.count()):
            #se definen los variables para ejecutar el comando
            item = self.list_widget.item(index)
            self.script = item.text()
            self.nuke_executable = r'"C:\Program Files\Nuke14.0v4\Nuke14.0"'  # Ruta al ejecutable de Nuke
            print(self.nuke_executable)
            command = self.nuke_executable + " -X " + f"Write{self.write} " + self.script
            print (command)
            
            if not count == 0:
                final_command = final_command + union + command
            else:
                final_command = command
            
            count = count + 1
        print(final_command)
        
        #Se inicia la clase RenderThread
        self.thread = RenderThread()
        
        #Se conectan las señales y lo que ejecutaran  
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.rendering_finished)

        #Se inicia el metodo que inicia el render
        self.thread.start_rendering(final_command)

        #Se establece el status como render in progress
        self.render_button.setEnabled(False)  # Deshabilitar el botón de renderizado
        self.render_in_progress = True  # Establecer el indicador de renderizado en progreso
        self.proceso.setText("Comenzando") #Establece el texto que va debajo de la barra de progreso

    #Actualiza la barra de progresso durante el render
    def update_progress(self, progress):
        self.progressBar.setValue(progress)
        self.proceso.setText("Renderizando")

    #Se activa una vez el render haya terminado
    def rendering_finished(self):
        self.proceso.setText("Render finalizado")
        self.render_button.setEnabled(True)  # Habilitar el botón de renderizado
        self.render_in_progress = False  # Establecer el indicador de renderizado en progreso en False


##################################################################################


class RenderThread(QtCore.QThread):
    progress = QtCore.Signal(int)
    finished = QtCore.Signal()

    def __init__(self):
        super().__init__()

    def start_rendering(self, comando):
        self.comando = comando
        self.start()


    def run(self):
        self.comando = [self.comando]
        print(self.comando)
        with subprocess.Popen(self.comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              universal_newlines=True) as proceso:
            while True:
                linea = proceso.stdout.readline()
                if not linea:
                    break
                print(linea)
                if "Frame" in linea:
                    patron = r"\((\d+) of (\d+)\)"
                    resultado = re.search(patron, linea)
                    progreso_actual = int(resultado.group(1))
                    frame_range = int(resultado.group(2))
                    porcentaje = (progreso_actual / frame_range) * 100
                    self.progress.emit(porcentaje)

        # Cuando se llega aqui es por que el proceso de render terminó            
        self.finished.emit()

      
##################################################################################
  
#Crear una clase de lista para manejar las funciones de la QListWidget
class FileListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                file_path = url.toLocalFile()
                item = QListWidgetItem(file_path)
                self.addItem(item)



##################################################################################
#ejecutable
##################################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())




