# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt,
    SIGNAL)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform, QPen)
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QSizePolicy,
    QSlider, QWidget, QMessageBox, QDialog,
    QVBoxLayout, QHBoxLayout, QPushButton)

color = [Qt.yellow, Qt.red, Qt.yellow]
rangeFont = QFont('Arial', 1)

class RatioDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.resize(250, 100)
        self.setFixedSize(250, 100)

        self.label0 = QLabel('', self)
        self.label0.setFont(rangeFont)
        self.label0.setGeometry(QRect(0, 0, 200, 30))
        self.label0.setStyleSheet("background-color: yellow;")

        self.show()


class Ui_MainWindow(object):
    # setupUi
    def setupUi(self, MainWindow):
        # default value
        global stuffValue
        stuffValue = ['100', '100', '100']
        self._ratioDialog = None

        if not MainWindow.objectName():
            MainWindow.setObjectName(u"Spoon")
        self.window = MainWindow
        self.window.resize(260, 190)
        self.window.setFixedSize(260, 190)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.window.sizePolicy().hasHeightForWidth())
        self.window.setSizePolicy(sizePolicy)
        self.window.setWindowOpacity(1.000000000000000)

        self.actionSettings = QAction(self.window)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionExit = QAction(self.window)
        self.actionExit.setObjectName(u"actionExit")
        self.actionRatio = QAction(self.window)
        self.actionRatio.setObjectName(u"actionRatio")
        self.centralwidget = QWidget(self.window)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())

        self.centralwidget.setSizePolicy(sizePolicy)
        self.ratioBox = QGroupBox(self.centralwidget)
        self.ratioBox.setObjectName(u"ratioBox")
        self.ratioBox.setGeometry(QRect(20, 0, 221, 81))

        # stuff label
        self.stuffLabel0 = QLabel(self.ratioBox)
        self.stuffLabel0.setObjectName(u"stuffLabel0")
        self.stuffLabel0.setGeometry(QRect(20, 30, 41, 16))
        self.stuffLabel1 = QLabel(self.ratioBox)
        self.stuffLabel1.setObjectName(u"stuffLabel1")
        self.stuffLabel1.setGeometry(QRect(90, 30, 41, 16))
        self.stuffLabel2 = QLabel(self.ratioBox)
        self.stuffLabel2.setObjectName(u"stuffLabel2")
        self.stuffLabel2.setGeometry(QRect(160, 30, 41, 16))

        # stuff input
        self.stuffInput0 = QLineEdit(self.ratioBox)
        self.stuffInput0.setObjectName(u"stuffInput0")
        self.stuffInput0.setGeometry(QRect(20, 50, 41, 20))
        self.stuffInput1 = QLineEdit(self.ratioBox)
        self.stuffInput1.setObjectName(u"stuffInput1")
        self.stuffInput1.setGeometry(QRect(90, 50, 41, 20))
        self.stuffInput2 = QLineEdit(self.ratioBox)
        self.stuffInput2.setObjectName(u"stuffInput2")
        self.stuffInput2.setGeometry(QRect(160, 50, 41, 20))

        # set default value
        self.stuffInput0.setText(stuffValue[0])
        self.stuffInput1.setText(stuffValue[1])
        self.stuffInput2.setText(stuffValue[2])

        # opacity slider
        self.opacityBox = QGroupBox(self.centralwidget)
        self.opacityBox.setObjectName(u"opacityBox")
        self.opacityBox.setGeometry(QRect(20, 90, 221, 61))

        self.opacitySlider = QSlider(self.opacityBox)
        self.opacitySlider.setObjectName(u"opacitySlider")
        self.opacitySlider.setGeometry(QRect(20, 30, 180, 20))
        self.opacitySlider.setSliderPosition(0)
        self.opacitySlider.setOrientation(Qt.Horizontal)

        self.window.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self.window)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 260, 24))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.window.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionRatio)
        self.menu.addAction(self.actionSettings)
        self.menu.addSeparator()
        self.menu.addAction(self.actionExit)

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self.window)

        # Actions
        self.opacitySlider.valueChanged.connect(self.onOpacityChanged)
        self.actionRatio.triggered.connect(self.openRatioDialog)
        self.actionExit.triggered.connect(QCoreApplication.instance().quit)

    def openRatioDialog(self):
        if self._ratioDialog is None:
            self._ratioDialog = RatioDialog()

    def onOpacityChanged(self):
        self.window.setWindowOpacity(1 - (self.opacitySlider.value() * 0.008))

    # retranslateUi
    def retranslateUi(self):
        self.window.setWindowTitle(QCoreApplication.translate("Spoon", u"Spoon", None))
        self.actionSettings.setText(QCoreApplication.translate("Spoon", u"\uc124\uc815", None))
        self.actionExit.setText(QCoreApplication.translate("Spoon", u"\uc885\ub8cc", None))
        self.actionRatio.setText(QCoreApplication.translate("Spoon", u"\ube44\uc728 \ucc3d \ubcf4\uae30", None))
        self.ratioBox.setTitle(QCoreApplication.translate("Spoon", u"\ube44\uc728", None))
        # if QT_CONFIG(tooltip)
        self.stuffLabel0.setToolTip(QCoreApplication.translate("Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
        # endif // QT_CONFIG(tooltip)
        self.stuffLabel0.setText(QCoreApplication.translate("Spoon", u"<html><head/><body><p align=\"center\">\uc7ac\ub8cc 1</p></body></html>", None))
        # if QT_CONFIG(tooltip)
        self.stuffLabel2.setToolTip(QCoreApplication.translate("Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
        # endif // QT_CONFIG(tooltip)
        self.stuffLabel2.setText(QCoreApplication.translate("Spoon", u"<html><head/><body><p align=\"center\">\uc7ac\ub8cc 3</p></body></html>", None))
        # if QT_CONFIG(tooltip)
        self.stuffLabel1.setToolTip(QCoreApplication.translate("Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
        # endif // QT_CONFIG(tooltip)
        self.stuffLabel1.setText(QCoreApplication.translate("Spoon", u"<html><head/><body><p align=\"center\">\uc7ac\ub8cc 2</p></body></html>", None))
        self.opacityBox.setTitle(QCoreApplication.translate("Spoon", u"\ud22c\uba85\ub3c4", None))
        self.menu.setTitle(QCoreApplication.translate("Spoon", u"\uba54\ub274", None))

