# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QProgressBar,
    QPushButton, QSizePolicy, QWidget)

class Ui_Nuke_Render(object):
    def setupUi(self, Nuke_Render):
        if not Nuke_Render.objectName():
            Nuke_Render.setObjectName(u"Nuke_Render")
        Nuke_Render.resize(806, 870)
        Nuke_Render.setAcceptDrops(True)
        self.frame = QFrame(Nuke_Render)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(20, 30, 631, 771))
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.input_write = QLineEdit(self.frame)
        self.input_write.setObjectName(u"input_write")
        self.input_write.setGeometry(QRect(30, 60, 551, 31))
        self.input_write.setAcceptDrops(False)
        self.input_write.setLocale(QLocale(QLocale.Spanish, QLocale.LatinAmericaAndTheCaribbean))
        self.input_write.setClearButtonEnabled(True)
        self.proceso = QLabel(self.frame)
        self.proceso.setObjectName(u"proceso")
        self.proceso.setGeometry(QRect(120, 620, 371, 51))
        self.proceso.setAlignment(Qt.AlignCenter)
        self.progressBar = QProgressBar(self.frame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(40, 480, 549, 19))
        self.progressBar.setValue(0)
        self.render_button = QPushButton(self.frame)
        self.render_button.setObjectName(u"render_button")
        self.render_button.setGeometry(QRect(190, 570, 231, 18))
        font = QFont()
        font.setFamilies([u"Poppins"])
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        self.render_button.setFont(font)
        self.render_button.setMouseTracking(False)
        self.render_button.setAutoFillBackground(False)
        self.render_button.setFlat(False)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(240, 420, 121, 21))
        self.label.setAlignment(Qt.AlignCenter)
        self.listWidget = QListWidget(self.frame)
        __qlistwidgetitem = QListWidgetItem(self.listWidget)
        __qlistwidgetitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        QListWidgetItem(self.listWidget)
        __qlistwidgetitem1 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem1.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled|Qt.ItemIsTristate);
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(30, 100, 551, 311))
        self.listWidget.setTabletTracking(True)
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setInputMethodHints(Qt.ImhNone)
        self.listWidget.setFrameShadow(QFrame.Raised)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setDragDropOverwriteMode(True)
        self.listWidget.setDragDropMode(QAbstractItemView.DragDrop)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listWidget.setSelectionRectVisible(True)
        self.listWidget.setSortingEnabled(True)
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(510, 430, 56, 17))
        self.pushButton.setAutoFillBackground(False)
        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(440, 430, 56, 17))

        self.retranslateUi(Nuke_Render)
        self.pushButton_2.clicked.connect(self.listWidget.doItemsLayout)
        self.pushButton.clicked.connect(self.listWidget.clearSelection)

        self.render_button.setDefault(False)


        QMetaObject.connectSlotsByName(Nuke_Render)
    # setupUi

    def retranslateUi(self, Nuke_Render):
        Nuke_Render.setWindowTitle(QCoreApplication.translate("Nuke_Render", u"Nuke Render", None))
        self.input_write.setPlaceholderText(QCoreApplication.translate("Nuke_Render", u"Nombre del Write", None))
        self.proceso.setText(QCoreApplication.translate("Nuke_Render", u"Cargue los archivos y haga click en renderizar", None))
        self.render_button.setText(QCoreApplication.translate("Nuke_Render", u"Renderizar", None))
        self.label.setText(QCoreApplication.translate("Nuke_Render", u"Render", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Nuke_Render", u"545645", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Nuke_Render", u"fdsafsadfasd", None));
        ___qlistwidgetitem2 = self.listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("Nuke_Render", u"fdsafsdafd", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

        self.pushButton.setText(QCoreApplication.translate("Nuke_Render", u"Remove", None))
        self.pushButton_2.setText(QCoreApplication.translate("Nuke_Render", u"Add", None))
    # retranslateUi

