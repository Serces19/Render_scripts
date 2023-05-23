import subprocess
import re
from tqdm import tqdm
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QProgressBar, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget
from PySide2 import QtWidgets, QtCore
from controladores.main_ui import Ui_Form
from PySide2.QtWidgets import QApplication, QMainWindow, QListView, QVBoxLayout, QWidget, QAbstractItemView, QListWidgetItem, QListWidget
from PySide2.QtCore import Qt, QMimeData, QUrl
import time


##################################################################################
#Clases de la interfaz
##################################################################################

class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        print('iniciando')
        
        #Setear cosas
        self.render_button.clicked.connect(self.renderizar)
        self.render_in_progress = False
        self.render_queue = []  # Lista para almacenar los scripts de Nuke
        
        #Crear lista y añadirla al layout
        self.list_widget = FileListWidget(self)
        self.gridLayout.addWidget(self.list_widget)
        print('layout')


    def renderizar(self):
        #Si hay un render en progreso este metodo no se puede ejecutar
        print(self.render_in_progress)
        if self.render_in_progress:
            print('vuelve')
            return
        
        self.render_queue = []
        self.write = self.input_write.text()
        print('el queue es: ', self.render_queue)

        #Comenzar un bucle que renderiza todos los items en la lista
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            self.script = item.text()
            self.render_queue.append(self.script)  # Agregar el script a la cola de renderizado

            if self.render_queue:
                print('dentro el ciclo for el queue es: ', self.render_queue)
                self.start_render()  # Iniciar el renderizado del primer script en la cola



    def start_render(self):
        print('start render', self.render_queue)
        if self.render_queue:
            print('desde el if del star render')
            script = self.render_queue.pop(0)  # Obtener el primer script de la cola
            self.thread = RenderThread()
            self.thread.progress.connect(self.update_progress)
            self.thread.finished.connect(self.rendering_finished)
            self.thread.start_rendering(script, self.write)
            self.render_button.setEnabled(False)  # Deshabilitar el botón de renderizado
            self.render_in_progress = True  # Establecer el indicador de renderizado en progreso
            self.proceso.setText("Comenzando")
        else:
            self.rendering_finished




    # def start_next_render(self):
    #     if self.render_queue:
    #         script = self.render_queue.pop(0)  # Obtener el primer script de la cola
    #         self.thread = RenderThread()
    #         self.thread.progress.connect(self.update_progress)
    #         self.thread.finished.connect(self.rendering_finished)
    #         self.thread.render_finished.connect(self.start_next_render)  # Conectar la señal render_finished al método start_next_render
    #         self.thread.start_rendering(script, self.write)
    #         self.render_button.setEnabled(False)  # Deshabilitar el botón de renderizado
    #         self.render_in_progress = True  # Establecer el indicador de renderizado en progreso
    #         self.proceso.setText("Comenzando")




    def update_progress(self, progress):
        self.progressBar.setValue(progress)

    def rendering_finished(self):
        # Realizar acciones adicionales después de que finalice el renderizado
        self.proceso.setText("Render finalizado")
        self.render_button.setEnabled(True)  # Habilitar el botón de renderizado
        self.render_in_progress = False  # Establecer el indicador de renderizado en progreso en False


        if not self.render_queue:
            self.close_application()
            
        else:    
            self.start_render()  # Iniciar el renderizado del siguiente script en la cola (si hay más)

    def close_application(self):
        # Cerrar la aplicación
        QApplication.quit()


##################################################################################


class RenderThread(QtCore.QThread):
    progress = QtCore.Signal(int)
    finished = QtCore.Signal()
    render_finished = QtCore.Signal()

    def __init__(self):
        super().__init__()

    def start_rendering(self, nk_file, write_node_index=1):
        self.nk_file = nk_file
        self.write_node_index = write_node_index
        self.nuke_executable = r"C:\Program Files\Nuke14.0v4\Nuke14.0"  # Ruta al ejecutable de Nuke
        print(self.nk_file,'start rendering')
        self.start()


    def run(self):
        command = [self.nuke_executable, "-X", f"Write{self.write_node_index}", self.nk_file]
        print(self.nk_file, 'run')
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              universal_newlines=True) as proceso:
            print('before forloop')
            print(proceso)
            print(proceso.stdout)

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


            # for linea in proceso.stdout:
            #     if "Frame" in linea:
            #         patron = r"\((\d+) of (\d+)\)"
            #         resultado = re.search(patron, linea)
            #         progreso_actual = int(resultado.group(1))
            #         frame_range = int(resultado.group(2))
            #         porcentaje = (progreso_actual / frame_range) * 100
            #         self.progress.emit(porcentaje)
            #         print(self.nk_file, 'subproceso')
        
        self.finished.emit()
        self.render_finished.emit()

        
##################################################################################

#Crear una clase de lista para manejar sus funciones
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


##################################################################
#ejecutar

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


