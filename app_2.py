import subprocess
import re
from tqdm import tqdm
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QProgressBar, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget
from PySide2 import QtWidgets, QtCore
from controladores.main_ui import Ui_Form
from PySide2.QtWidgets import QApplication, QMainWindow, QListView, QVBoxLayout, QWidget, QAbstractItemView, QListWidgetItem, QListWidget
from PySide2.QtCore import Qt, QMimeData, QUrl



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



class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        #Setear cosas
        self.render_button.clicked.connect(self.renderizar)
        
        #Crear lista
        self.list_widget = FileListWidget(self)
        self.gridLayout.addWidget(self.list_widget)


    def renderizar(self):
        self.write = self.input_write.text()
        #self.script = self.list_widget.text()

        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            nombre_item = item.text()
            # Realizar acciones con el nombre del item
            print(nombre_item)  # Ejemplo de acción: imprimir el nombre del item


        # self.thread = RenderThread()
        # self.thread.progress.connect(self.update_progress)
        # self.thread.finished.connect(self.rendering_finished)
        # self.thread.start_rendering(self.script, self.write)

    def update_progress(self, progress):
        self.progressBar.setValue(progress)

    def rendering_finished(self):
        # Realizar acciones adicionales después de que finalice el renderizado
        self.proceso.setText("Render finalizado")


class RenderThread(QtCore.QThread):
    progress = QtCore.Signal(int)
    finished = QtCore.Signal()

    def __init__(self):
        super().__init__()

    def start_rendering(self, nk_file, write_node_index=1):
        self.nk_file = nk_file
        self.write_node_index = write_node_index
        self.nuke_executable = r"C:\Program Files\Nuke14.0v4\Nuke14.0"  # Ruta al ejecutable de Nuke
        self.start()

    def run(self):
        self.proceso.setText("Comenzando")
        command = [self.nuke_executable, "-X", f"Write{self.write_node_index}", self.nk_file]

        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              universal_newlines=True) as proceso:
            for linea in proceso.stdout:
                if "Frame" in linea:
                    patron = r"\((\d+) of (\d+)\)"
                    resultado = re.search(patron, linea)
                    progreso_actual = int(resultado.group(1))
                    frame_range = int(resultado.group(2))
                    porcentaje = (progreso_actual / frame_range) * 100
                    self.progress.emit(porcentaje)

        self.finished.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
