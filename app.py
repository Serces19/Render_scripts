import subprocess
from tqdm import tqdm
import re
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QProgressBar, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget
from PySide2 import QtWidgets, QtCore
from controladores.main_ui import Ui_Form


# # Ejemplo de uso
# archivo_nk = r"C:\Users\sergi\Desktop\pruebas\pruebas.nk"
# indice_nodo_write = 1
# renderizar_nodo_write(archivo_nk, indice_nodo_write)


class MainWindow(QMainWindow ,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.render_button.clicked.connect(self.rederizar)

    def rederizar(self):
        self.write = self.input_write.text()
        self.script = self.input_script.text()
        print(self.script, self.write, 'hola')

        self.thread = RenderThread()
        self.thread.progress.connect(self.update_progress)
        self.thread.start()
        self.thread.renderizar_nodo_write(self.script, self.write)


    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

        

class RenderThread(QtCore.QThread):
    progress = QtCore.Signal(int)
    def __init__(self):
        super().__init__()
            
    def renderizar_nodo_write(self, nk_file, write_node_index=1):
        nuke_executable = r"C:\Program Files\Nuke14.0v4\Nuke14.0"  # Ruta al ejecutable de Nuke
        nk_file = f"{nk_file}"
        nk_file = r"" + nk_file
        command = [nuke_executable, "-X", f"Write{write_node_index}", nk_file]
        
        with tqdm(total=0, ncols=80, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            proceso = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for linea in proceso.stdout:
                # Analizar la salida del proceso para detectar el progreso y actualizar la barra de progreso
                # Aquí puedes personalizar cómo se actualiza el progreso según la salida de Nuke
                if "Frame" in linea:
                    patron = r"\((\d+) of (\d+)\)"
                    resultado = re.search(patron, linea)
                    progreso_actual = int(resultado.group(1))
                    frame_range = int(resultado.group(2))
                    if pbar.total == 0:
                        pbar.reset(total=frame_range)
                    pbar.update(progreso_actual - pbar.n)
                    porcentaje = (progreso_actual/frame_range)*100
                    self.progress.emit(porcentaje)
            proceso.wait()


    def terminate(self) -> None:
        return super().terminate()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())




