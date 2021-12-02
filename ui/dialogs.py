# -*- coding: utf-8 -*-

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

color = ['#FFFF00', '#FF0000', '#FFFF00']
rangeFont = QFont('Arial', 1)


class RatioDialog(QMainWindow):
    def __init__(self, currentValue):
        super().__init__()
        self.currentWindowSize = {
            'width': 245,
            'height': 10
        }
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.ratio = currentValue
        self.initUI()

    # 새로운 값을 계산 후 반영
    def calculate(self):
        list = []
        sum = 0
        temp = 0

        for value in self.ratio:
            sum += value

        perValue = self.currentWindowSize['width'] / sum

        for ratioValue in self.ratio:
            if ratioValue == 0:
                continue
            list.append(perValue * ratioValue)

        for i in range(0, len(list)):
            self.labels[i].setGeometry(QRect(temp, 0, temp + list[i], 10))
            self.labels[i].setStyleSheet("background-color: " + color[i] + ";")

            temp += list[i]

    # 저장된 값을 업데이트
    def update(self, newValue):
        self.ratio = newValue
        self.calculate()

    # UI 요소 초기화
    def initUI(self):
        self.resize(self.currentWindowSize['width'],
                    self.currentWindowSize['height'])
        self.setFixedSize(
            self.currentWindowSize['width'], self.currentWindowSize['height'])
        self.labels = [
            QLabel('', self),
            QLabel('', self),
            QLabel('', self),
        ]

        for i in range(0, 3):
            self.labels[i].setFont(rangeFont)

        self.calculate()
        self.show()

    # 마우스 클릭 이벤트
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # Change mouse icon

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        self._ratioDialog = None
        self.resize(260, 190)
        self.setFixedSize(260, 190)

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.actionSettings = QAction(self)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionExit = QAction(self)
        self.actionExit.setObjectName(u"actionExit")
        self.actionRatio = QAction(self)
        self.actionRatio.setObjectName(u"actionRatio")
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth())

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
        self.stuffInput0.setText('100')
        self.stuffInput1.setText('100')
        self.stuffInput2.setText('100')

        # opacity slider
        self.opacityBox = QGroupBox(self.centralwidget)
        self.opacityBox.setObjectName(u"opacityBox")
        self.opacityBox.setGeometry(QRect(20, 90, 221, 61))

        self.opacitySlider = QSlider(self.opacityBox)
        self.opacitySlider.setObjectName(u"opacitySlider")
        self.opacitySlider.setGeometry(QRect(20, 30, 180, 20))
        self.opacitySlider.setSliderPosition(70)
        self.opacitySlider.setOrientation(Qt.Horizontal)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 260, 24))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionRatio)
        self.menu.addAction(self.actionSettings)
        self.menu.addSeparator()
        self.menu.addAction(self.actionExit)

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)

        self.m_flag = False

        # Actions
        self.opacitySlider.valueChanged.connect(self.onOpacityChanged)
        self.actionRatio.triggered.connect(self.openRatioDialog)
        self.actionExit.triggered.connect(QCoreApplication.instance().quit)

    def openRatioDialog(self):
        data = [
            int(self.stuffInput0.text()),
            int(self.stuffInput1.text()),
            int(self.stuffInput2.text())
        ]
        if self._ratioDialog is None:
            self._ratioDialog = RatioDialog(data)
        else:
            self._ratioDialog.update(data)

    def onOpacityChanged(self):
        if self._ratioDialog is not None:
            self._ratioDialog.setWindowOpacity(
                1 - (self.opacitySlider.value() * 0.008))

    # retranslateUi
    def retranslateUi(self):
        self.setWindowTitle(
            QCoreApplication.translate("Spoon", u"Spoon", None))
        self.actionSettings.setText(
            QCoreApplication.translate("Spoon", u"\uc124\uc815", None))
        self.actionExit.setText(QCoreApplication.translate(
            "Spoon", u"\uc885\ub8cc", None))
        self.actionRatio.setText(QCoreApplication.translate(
            "Spoon", u"\ube44\uc728 \ucc3d \ubcf4\uae30", None))
        self.ratioBox.setTitle(QCoreApplication.translate(
            "Spoon", u"\ube44\uc728", None))

        # if QT_CONFIG(tooltip)
        self.stuffLabel0.setToolTip(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
        # endif // QT_CONFIG(tooltip)
        self.stuffLabel0.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p align=\"center\">\uc7ac\ub8cc 1</p></body></html>", None))

        # if QT_CONFIG(tooltip)
        self.stuffLabel1.setToolTip(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
        # endif // QT_CONFIG(tooltip)
        self.stuffLabel1.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p align=\"center\">\uc7ac\ub8cc 2</p></body></html>", None))

        # if QT_CONFIG(tooltip)
        self.stuffLabel2.setToolTip(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
        # endif // QT_CONFIG(tooltip)
        self.stuffLabel2.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p align=\"center\">\uc7ac\ub8cc 3</p></body></html>", None))

        self.opacityBox.setTitle(QCoreApplication.translate(
            "Spoon", u"\ud22c\uba85\ub3c4", None))
        self.menu.setTitle(QCoreApplication.translate(
            "Spoon", u"\uba54\ub274", None))
