# -*- coding: utf-8 -*-
'''
# Mini window for Spoon
# https://github.com/kry-p/Teaspoon-mabinogi
'''

from PySide6.QtCore import (QMetaObject, QRect, QSize, Qt)
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QGroupBox, QLabel, QLineEdit, QMainWindow, QMenu, 
                               QMenuBar, QPushButton, QWidget)

from modules.elements import Widget

PERCENT_COLOR = '#AAAAAA'
NAME_LABEL_STYLESHEET = 'font-weight: 600;'

# Mini window
class MiniWindow(QMainWindow):
    def __init__(self, APP_VERSION):
        super().__init__()

        # Settings for window
        self.APP_VERSION = APP_VERSION
        self.setWindowTitle('Spoon %s' % self.APP_VERSION)
        self.resize(190, 190)
        self.setFixedSize(QSize(190, 190))
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # Menu bar
        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 190, 22))

        self.toolsMenu = QMenu(self.menuBar)
        self.toolsMenu.setTitle('도구')
        self.setMenuBar(self.menuBar)
        self.menuBar.addAction(self.toolsMenu.menuAction())
        self.actions = {
            'lockRatioBar': Widget(widget = QAction(self),
                                   text = "비율 바 잠금"),
            'changeMode': Widget(widget = QAction(self),
                                 text = "모드 변경"),
            'settings': Widget(widget = QAction(self),
                               text = "설정"),
            'help': Widget(widget = QAction(self),
                           text = "도움말"),
        }
        self.actions['lockRatioBar'].getWidget().setCheckable(True)

        self.toolsMenu.addAction(self.actions['lockRatioBar'].getWidget())
        self.toolsMenu.addAction(self.actions['changeMode'].getWidget())
        self.toolsMenu.addSeparator()
        self.toolsMenu.addAction(self.actions['settings'].getWidget())
        self.toolsMenu.addAction(self.actions['help'].getWidget())

        # Ratio box
        self.ratioBox = Widget(widget = QGroupBox(self.centralWidget),
                               title = '비율',
                               geometry = QRect(10, 10, 171, 111))
    
        # Stuff labels
        self.stuffLabels = [
            Widget(widget = QLabel(self.ratioBox), geometry = QRect(20, 22, 41, 20), text = '재료 1'),
            Widget(widget = QLabel(self.ratioBox), geometry = QRect(20, 52, 41, 20), text = '재료 2'),
            Widget(widget = QLabel(self.ratioBox), geometry = QRect(20, 82, 41, 20), text = '재료 3'),
            Widget(widget = QLabel(self.ratioBox), geometry = QRect(140, 22, 21, 20), text = '%'),
            Widget(widget = QLabel(self.ratioBox), geometry = QRect(140, 52, 21, 20), text = '%'),
            Widget(widget = QLabel(self.ratioBox), geometry = QRect(140, 82, 21, 20), text = '%'),
        ]

        for i in range(0, 3):
            self.stuffLabels[i].setStyleSheet(NAME_LABEL_STYLESHEET)
            self.stuffLabels[i].setAlignment(Qt.AlignCenter)
        for i in range(3, 6):
            self.stuffLabels[i].setStyleSheet('color: %s;' % PERCENT_COLOR)

        # Stuff inputs
        self.stuffInput0 = QLineEdit(self.ratioBox)
        self.stuffInput0.setGeometry(QRect(95, 20, 41, 20))
        self.stuffInput1 = QLineEdit(self.ratioBox)
        self.stuffInput1.setGeometry(QRect(95, 50, 41, 20))
        self.stuffInput2 = QLineEdit(self.ratioBox)
        self.stuffInput2.setGeometry(QRect(95, 80, 41, 20))
        
        self.ratioBarButton = Widget(widget = QPushButton(self.centralWidget),
                                     geometry = QRect(10, 130, 171, 31),
                                     text = '비율 바 On / Off')
        
        QMetaObject.connectSlotsByName(self)

  