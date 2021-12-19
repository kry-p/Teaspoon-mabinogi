# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'spoon_0.1.1_mini.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
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
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QWidget)

class MiniWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()

        if not self.objectName():
            self.setObjectName(u"Spoon")
        self.resize(190, 190)
        self.setMinimumSize(QSize(190, 190))
        self.setMaximumSize(QSize(190, 190))
        self.action = QAction(self)
        self.action.setObjectName(u"action")
        self.action.setCheckable(True)
        self.action_2 = QAction(self)
        self.action_2.setObjectName(u"action_2")
        self.action_4 = QAction(self)
        self.action_4.setObjectName(u"action_4")
        self.action_5 = QAction(self)
        self.action_5.setObjectName(u"action_5")
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        self.ratiobox = QGroupBox(self.centralwidget)
        self.ratiobox.setObjectName(u"ratiobox")
        self.ratiobox.setGeometry(QRect(10, 10, 171, 111))
        self.Tind2_2 = QLabel(self.ratiobox)
        self.Tind2_2.setObjectName(u"Tind2_2")
        self.Tind2_2.setGeometry(QRect(20, 52, 41, 20))
        self.Tind3_2 = QLabel(self.ratiobox)
        self.Tind3_2.setObjectName(u"Tind3_2")
        self.Tind3_2.setGeometry(QRect(20, 82, 41, 20))
        self.stuff1_2 = QLineEdit(self.ratiobox)
        self.stuff1_2.setObjectName(u"stuff1_2")
        self.stuff1_2.setGeometry(QRect(95, 20, 41, 20))
        self.stuff2_2 = QLineEdit(self.ratiobox)
        self.stuff2_2.setObjectName(u"stuff2_2")
        self.stuff2_2.setGeometry(QRect(95, 50, 41, 20))
        self.Tind1_2 = QLabel(self.ratiobox)
        self.Tind1_2.setObjectName(u"Tind1_2")
        self.Tind1_2.setGeometry(QRect(20, 22, 41, 20))
        self.stuff3_2 = QLineEdit(self.ratiobox)
        self.stuff3_2.setObjectName(u"stuff3_2")
        self.stuff3_2.setGeometry(QRect(95, 80, 41, 20))
        self.s2p_2 = QLabel(self.ratiobox)
        self.s2p_2.setObjectName(u"s2p_2")
        self.s2p_2.setGeometry(QRect(140, 52, 21, 20))
        self.s3p_2 = QLabel(self.ratiobox)
        self.s3p_2.setObjectName(u"s3p_2")
        self.s3p_2.setGeometry(QRect(140, 82, 21, 20))
        self.s1p_2 = QLabel(self.ratiobox)
        self.s1p_2.setObjectName(u"s1p_2")
        self.s1p_2.setGeometry(QRect(140, 22, 21, 20))
        self.ratioswitch = QPushButton(self.centralwidget)
        self.ratioswitch.setObjectName(u"ratioswitch")
        self.ratioswitch.setGeometry(QRect(10, 130, 171, 31))
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 190, 21))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_5)
        self.menu.addSeparator()
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_4)

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)

    # setupUi
    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Spoon", u"Spoon", None))
        self.action.setText(QCoreApplication.translate("Spoon", u"\ube44\uc728\ubc14 \uc7a0\uae08", None))
        self.action_2.setText(QCoreApplication.translate("Spoon", u"\uc124\uc815", None))
        self.action_4.setText(QCoreApplication.translate("Spoon", u"\ub3c4\uc6c0\ub9d0", None))
        self.action_5.setText(QCoreApplication.translate("Spoon", u"\ubaa8\ub4dc \ubcc0\uacbd", None))
        self.ratiobox.setTitle(QCoreApplication.translate("Spoon", u"\ube44\uc728", None))
#if QT_CONFIG(tooltip)
        self.Tind2_2.setToolTip(QCoreApplication.translate("Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.Tind2_2.setText(QCoreApplication.translate("Spoon", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">\uc7ac\ub8cc2</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.Tind3_2.setToolTip(QCoreApplication.translate("Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.Tind3_2.setText(QCoreApplication.translate("Spoon", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">\uc7ac\ub8cc3</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.Tind1_2.setToolTip(QCoreApplication.translate("Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.Tind1_2.setText(QCoreApplication.translate("Spoon", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">\uc7ac\ub8cc1</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.s2p_2.setToolTip(QCoreApplication.translate("Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.s2p_2.setText(QCoreApplication.translate("Spoon", u"<html><head/><body><p><span style=\" color:#aaaaaa;\">%</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.s3p_2.setToolTip(QCoreApplication.translate("Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.s3p_2.setText(QCoreApplication.translate("Spoon", u"<html><head/><body><p><span style=\" color:#aaaaaa;\">%</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.s1p_2.setToolTip(QCoreApplication.translate("Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.s1p_2.setText(QCoreApplication.translate("Spoon", u"<html><head/><body><p><span style=\" color:#aaaaaa;\">%</span></p></body></html>", None))
        self.ratioswitch.setText(QCoreApplication.translate("Spoon", u"\ube44\uc728\ubc14 On/Off", None))
        self.menu.setTitle(QCoreApplication.translate("Spoon", u"\ub3c4\uad6c", None))
    # retranslateUi

