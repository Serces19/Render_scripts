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

        self.setWindowTitle("Nuke render")
        self.setGeometry(100, 100, 800, 500)  # Definir posición y tamaño de la ventana
        self.setStyleSheet(u"background-color: rgb(20, 25, 35);\n"
                                    "font: 10pt \"Poppins\";\n"
                                    "color: rgb(180, 180, 180);")        
        self.center_window()

        #-------------------------------Crear-------------------------------
        # Crear el layout principal y el widget central
        layout = QVBoxLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Crear las divisiones principales (horizontal)
        division_H_layout1 = QHBoxLayout()
        division_H_layout2 = QHBoxLayout()
        division_H_layout3 = QHBoxLayout()
        division_H_layout4 = QHBoxLayout()
        division_H_layout5 = QHBoxLayout()

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
        division_H_layout5.addLayout(sub_division_layout9)

        # Agregar las divisiones principales al layout principal
        layout.addLayout(division_H_layout1)
        layout.addLayout(division_H_layout2)
        layout.addLayout(division_H_layout3)
        layout.addLayout(division_H_layout4)
        layout.addLayout(division_H_layout5)

        #-------------------------Crear los widgets, botones, etc---------------------------
        # Crear botones y asignar colores de fondo y estilo redondeado
        button1 = QPushButton("Botón 1")
        button1.setStyleSheet("background-color: rgb(23, 27, 35);")
        sub_division_layout1.addWidget(button1)

        label_1 = QLabel("label 1")
        label_1.setAlignment(Qt.AlignCenter)
        sub_division_layout2.addWidget(label_1)

        button2 = QPushButton("Botón 2")
        button2.setStyleSheet("background-color: rgb(70, 80, 90);")
        sub_division_layout3.addWidget(button2)

        
        input_write = QLineEdit()
        input_write.setPlaceholderText('input write')
        input_write.setAlignment(Qt.AlignCenter)
        sub_division_layout4.addWidget(input_write)

        label_lista = QLabel("Scripts a renderizar:")
        label_lista.setAlignment(Qt.AlignLeft)
        sub_division_layout5.addWidget(label_lista)

        # Agregar la lista
        lista = FileListWidget(self)
        sub_division_layout5.addWidget(lista)

        # Agregar el boton de render
        button5 = QPushButton("Render")
        button5.setStyleSheet("background-color: rgb(10, 80, 50);")
        sub_division_layout6.addWidget(button5)

        #Agregar botones de iliminar y agregar
        add_button = QPushButton("+")
        add_button.clicked.connect(lista.add_item)
        child_sub_division_H_layout1.addWidget(add_button)

        remove_button = QPushButton("-")
        remove_button.clicked.connect(lista.remove_item)
        child_sub_division_H_layout1.addWidget(remove_button)

        label_3 = QLabel("Status:")
        label_3.setAlignment(Qt.AlignCenter)
        sub_division_layout8.addWidget(label_3)

        label_4 = QLabel("Tiempo:")
        label_4.setAlignment(Qt.AlignCenter)
        sub_division_layout9.addWidget(label_4)
        

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

        self.addItem("Elemento 1")
        self.addItem("Elemento 2")
        self.addItem("Elemento 3")
        self.addItem("Elemento 4")
        self.addItem("Elemento 5")

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



