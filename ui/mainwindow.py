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
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QSizePolicy,
    QSlider, QWidget, QMessageBox)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        self.window = MainWindow
        self.window.resize(260, 190)
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
        self.stuffInput2 = QLineEdit(self.ratioBox)
        self.stuffInput2.setObjectName(u"stuffInput2")
        self.stuffInput2.setGeometry(QRect(160, 50, 41, 20))
        self.stuffLabel0 = QLabel(self.ratioBox)
        self.stuffLabel0.setObjectName(u"stuffLabel0")
        self.stuffLabel0.setGeometry(QRect(20, 30, 41, 16))
        self.stuffLabel2 = QLabel(self.ratioBox)
        self.stuffLabel2.setObjectName(u"stuffLabel2")
        self.stuffLabel2.setGeometry(QRect(160, 30, 41, 16))
        self.stuffInput0 = QLineEdit(self.ratioBox)
        self.stuffInput0.setObjectName(u"stuffInput0")
        self.stuffInput0.setGeometry(QRect(20, 50, 41, 20))
        self.stuffLabel1 = QLabel(self.ratioBox)
        self.stuffLabel1.setObjectName(u"stuffLabel1")
        self.stuffLabel1.setGeometry(QRect(90, 30, 41, 16))
        self.stuffInput1 = QLineEdit(self.ratioBox)
        self.stuffInput1.setObjectName(u"stuffInput1")
        self.stuffInput1.setGeometry(QRect(90, 50, 41, 20))
        self.opacityBox = QGroupBox(self.centralwidget)
        self.opacityBox.setObjectName(u"opacityBox")
        self.opacityBox.setGeometry(QRect(20, 90, 221, 61))
        self.opacitySlider = QSlider(self.opacityBox)
        self.opacitySlider.setObjectName(u"opacitySlider")
        self.opacitySlider.setGeometry(QRect(20, 30, 180, 20))
        self.opacitySlider.setSliderPosition(70)
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

    # setupUi
    def openSub(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('서브윈도우')
        msgBox.setText('서브윈도우 창입니다.')

        msgBox.setInformativeText("InformativeText")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Discard | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Ok)

        result = msgBox.exec()
        if result == QMessageBox.Ok:
            print("OK")
        elif result == QMessageBox.Cancel:
            print("Cancel")
        elif result == QMessageBox.Discard:
            print("Discard")

    def onOpacityChanged(self):
        self.window.setWindowOpacity(1 - (self.opacitySlider.value() * 0.008))


    def retranslateUi(self):
        self.window.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"\uc124\uc815", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"\uc885\ub8cc", None))
        self.actionRatio.setText(QCoreApplication.translate("MainWindow", u"\ube44\uc728 \ucc3d \ubcf4\uae30", None))
        self.ratioBox.setTitle(QCoreApplication.translate("MainWindow", u"\ube44\uc728", None))
#if QT_CONFIG(tooltip)
        self.stuffLabel0.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.stuffLabel0.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\uc7ac\ub8cc 1</p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.stuffLabel2.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.stuffLabel2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\uc7ac\ub8cc 3</p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.stuffLabel1.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.stuffLabel1.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">\uc7ac\ub8cc 2</p></body></html>", None))
        self.opacityBox.setTitle(QCoreApplication.translate("MainWindow", u"\ud22c\uba85\ub3c4", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\uba54\ub274", None))
    # retranslateUi

