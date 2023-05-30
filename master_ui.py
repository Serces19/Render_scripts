import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2 import *
from PySide2.QtGui import QColor, QPalette
from PySide2.QtCore import Qt


################################################################################
# Interfaz
################################################################################

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
    
    def setupUi(self, Nuke_Render):
        if not Nuke_Render.objectName():
            Nuke_Render.setObjectName("Nuke Render")

        self.setWindowTitle("Nuke render")
        self.setGeometry(100, 100, 1000, 1000)  # Definir posición y tamaño de la ventana
        self.setStyleSheet(u"background-color: rgb(20, 25, 35);\n"
                                    "font: 9pt \"Poppins\";\n"
                                    "color: rgb(180, 180, 180);")        
        self.center_window()

        #-------------------------------Crear-------------------------------
        # Crear el layout principal y el widget central
        layout = QVBoxLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("QWidget { border-radius: 5px; padding: 10px; background-color: rgba(255, 255, 255, 5); }")

        # Crear las divisiones principales (horizontal)
        division_H_layout1 = QHBoxLayout()
        division_H_layout2 = QHBoxLayout()
        division_H_layout3 = QHBoxLayout()
        division_H_layout4 = QHBoxLayout()
        division_H_layout5 = QHBoxLayout()
        division_H_layout6 = QHBoxLayout()

        # Crear las divisiones secundarias (vertical)
        sub_division_layout1 = QVBoxLayout()
        sub_division_layout2 = QVBoxLayout()
        sub_division_layout3 = QVBoxLayout()
        sub_division_layout4 = QVBoxLayout()
        sub_division_layout5 = QVBoxLayout()
        sub_division_layout6 = QVBoxLayout()
        sub_division_layout7 = QVBoxLayout()
        sub_division_layout8 = QVBoxLayout()
        sub_division_layout9 = QVBoxLayout()
        sub_division_layout10 = QVBoxLayout()

        #Crear las child subdivisions
        child_sub_division_H_layout1 = QHBoxLayout()

        #-------------------------Agregar-------------------------------
        #Agregar las child subdivisions a las subdivisiones
        sub_division_layout7.addLayout(child_sub_division_H_layout1)

        # Agregar las divisiones secundarias a las divisiones principales
        division_H_layout1.addLayout(sub_division_layout1)
        division_H_layout1.addLayout(sub_division_layout2)
        division_H_layout1.addLayout(sub_division_layout3)

        division_H_layout2.addLayout(sub_division_layout4)

        division_H_layout3.addLayout(sub_division_layout5)

        division_H_layout4.addLayout(sub_division_layout6)
        division_H_layout4.addLayout(sub_division_layout7)

        division_H_layout5.addLayout(sub_division_layout8)

        division_H_layout6.addLayout(sub_division_layout9)
        division_H_layout6.addLayout(sub_division_layout10)

        # Agregar las divisiones principales al layout principal
        layout.addLayout(division_H_layout1)
        layout.addLayout(division_H_layout2)
        spacer = QSpacerItem(0, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer)
        layout.addLayout(division_H_layout3)
        layout.addItem(spacer)
        layout.addLayout(division_H_layout4)
        layout.addItem(spacer)
        layout.addLayout(division_H_layout5)
        layout.addLayout(division_H_layout6)

        #-------------------------Crear los widgets, botones, etc---------------------------
        # Crear botones y asignar colores de fondo y estilo redondeado
        self.nuke_dir = QLineEdit()
        self.nuke_dir.setPlaceholderText(r'C:\Program Files\Nuke14.0v4\Nuke14.0.exe')
        self.nuke_dir.setToolTip('Ubicación del archivo ejecutable de Nuke')
        sub_division_layout1.addWidget(self.nuke_dir)

        # label_1 = QLabel("label 1")
        # label_1.setAlignment(Qt.AlignCenter)
        # sub_division_layout2.addWidget(label_1)

        # button2 = QPushButton("Botón 2")
        # button2.setStyleSheet("background-color: rgb(70, 80, 90);")
        # sub_division_layout3.addWidget(button2)

        #para introducir el nombre del script
        self.input_write = QLineEdit()
        self.input_write.setPlaceholderText('Write1')
        self.input_write.setToolTip('Nombre del Write a renderizar')
        self.input_write.setAlignment(Qt.AlignLeft)
        sub_division_layout4.addWidget(self.input_write)
        
        #etiqueta de la lista
        label_lista = QLabel("Arrastra los scripts a renderizar:")
        label_lista.setAlignment(Qt.AlignLeft)
        sub_division_layout5.addWidget(label_lista)

        # Agregar la lista
        self.lista = FileListWidget(self)
        sub_division_layout5.addWidget(self.lista)

        # Agregar el boton de render
        self.render_button = QPushButton("Render")
        self.render_button.setStyleSheet("QPushButton { background-color: rgb(30, 120, 90); }"
                     "QPushButton:hover { background-color: rgb(40, 130, 100); }"
                     "QPushButton:pressed { background-color:rgb(10, 120, 120); }")

        sub_division_layout6.addWidget(self.render_button)

        #Agregar botones de add
        add_button = QPushButton("+")
        add_button.setStyleSheet("QPushButton:hover { background-color: rgb(40, 45, 60); }"
                                "QPushButton:pressed { background-color:rgb(50, 55, 70); }"
                                "QPushButton { font-size: 18px; font-weight: bold; }")
        add_button.clicked.connect(self.lista.add_item)
        child_sub_division_H_layout1.addWidget(add_button)

        #Agregar botones de eliminar 
        remove_button = QPushButton("-")
        remove_button.clicked.connect(self.lista.remove_item)
        remove_button.setStyleSheet("QPushButton:hover { background-color: rgb(40, 45, 60); }"
                                    "QPushButton:pressed { background-color:rgb(50, 55, 70); }"
                                    "QPushButton { font-size: 18px; font-weight: bold; }")
        child_sub_division_H_layout1.addWidget(remove_button)

        # Agregar la barra de progreso
        self.progressBar = QProgressBar()
        self.progressBar.setObjectName("progressBar")
        style = """
        QProgressBar::chunk {
            background-color: rgb(30, 120, 90);
        }
        """
        self.progressBar.setStyleSheet(style)
        self.progressBar.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        sub_division_layout8.addWidget(self.progressBar)

        #Label del status
        self.status = QLabel("Status:")
        self.status.setAlignment(Qt.AlignLeft)
        sub_division_layout9.addWidget(self.status)

        #Label de la descripcion del render
        self.descripcion = QLabel("-")
        self.descripcion.setAlignment(Qt.AlignLeft)
        self.descripcion.setStyleSheet("font-size: 7pt; color: rgb(90, 90, 90);")
        sub_division_layout9.addWidget(self.descripcion)

        #Label del tiempo total de render
        self.tiempo = QLabel("Tiempo:")
        self.tiempo.setAlignment(Qt.AlignLeft)
        sub_division_layout10.addWidget(self.tiempo)

        #Label del tiempo estimado de render
        self.tiempo_restante = QLabel("-")
        self.tiempo_restante.setAlignment(Qt.AlignLeft)
        sub_division_layout10.addWidget(self.tiempo_restante)


    def center_window(self):
        # Obtener el tamaño de la pantalla y el tamaño de la ventana
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()

        # Calcular la posición central de la ventana
        center_x = screen_geometry.center().x() - window_geometry.width() / 2
        center_y = screen_geometry.center().y() - window_geometry.height() / 2

        # Establecer la posición de la ventana
        self.move(center_x, center_y)


############################################################

class FileListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(1)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.setViewMode(QListView.ListMode)
        self.setItemDelegate(AlternatingColorDelegate())   

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

    def add_item(self):
        new_item_text = "Elemento {}".format(self.count() + 1)
        self.addItem(new_item_text)

    def remove_item(self):
        selected_items = self.selectedItems()
        for item in selected_items:
            self.takeItem(self.row(item))

################################################################################

class AlternatingColorDelegate(QStyledItemDelegate):

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if index.row() % 2 == 0:
            option.backgroundBrush = QColor(20, 30, 40)  # Color para filas pares
        else:
            option.backgroundBrush = QColor(25, 35, 45)  # Color para filas impares



################################################################################
# ejecutar
################################################################################

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())



