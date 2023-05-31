# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Nuke_Render(object):
    def setupUi(self, Nuke_Render):
        if not Nuke_Render.objectName():
            Nuke_Render.setObjectName(u"Nuke_Render")
        Nuke_Render.resize(806, 870)
        self.frame = QFrame(Nuke_Render)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(70, 30, 631, 771))
        self.frame.setStyleSheet(u"background-color: rgb(200, 200, 200);\n"
"font: 8pt \"Poppins\";\n"
"color: rgb(21, 21, 21);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.input_write = QLineEdit(self.frame)
        self.input_write.setObjectName(u"input_write")
        self.input_write.setGeometry(QRect(40, 210, 551, 31))
        self.input_write.setAcceptDrops(False)
        self.proceso = QLabel(self.frame)
        self.proceso.setObjectName(u"proceso")
        self.proceso.setGeometry(QRect(200, 640, 231, 20))
        self.proceso.setAlignment(Qt.AlignCenter)
        self.layoutWidget = QWidget(self.frame)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(40, 270, 551, 311))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.progressBar = QProgressBar(self.layoutWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)

        self.render_button = QPushButton(self.layoutWidget)
        self.render_button.setObjectName(u"render_button")
        font = QFont()
        font.setFamily(u"Poppins")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.render_button.setFont(font)
        self.render_button.setMouseTracking(False)
        self.render_button.setAutoFillBackground(False)
        self.render_button.setFlat(False)

        self.gridLayout.addWidget(self.render_button, 4, 0, 1, 1)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 0, 1, 1)


        self.retranslateUi(Nuke_Render)

        self.render_button.setDefault(False)


        QMetaObject.connectSlotsByName(Nuke_Render)
    # setupUi

    def retranslateUi(self, Nuke_Render):
        Nuke_Render.setWindowTitle(QCoreApplication.translate("Nuke_Render", u"Nuke Render", None))
        self.input_write.setPlaceholderText(QCoreApplication.translate("Nuke_Render", u"Nombre del Write", None))
        self.proceso.setText(QCoreApplication.translate("Nuke_Render", u"Cargue los archivos y haga click en renderizar", None))
        self.render_button.setText(QCoreApplication.translate("Nuke_Render", u"Renderizar", None))
        self.label.setText(QCoreApplication.translate("Nuke_Render", u"Render", None))
    # retranslateUi

