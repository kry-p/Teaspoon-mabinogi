# -*- coding: utf-8 -*-
'''
# Mini window for Spoon
# https://github.com/kry-p/Teaspoon-mabinogi
'''

from PyQt5.QtCore import (QEvent, QMetaObject, QRect, QSize, Qt)
from PyQt5.QtWidgets import (QGroupBox, QLabel, QLineEdit, QMainWindow, 
                             QMenu, QMenuBar, QPushButton, QWidget,
                             QAction)

from modules.elements import Widget
from .preferences_provider import (preferences, getPreferences, watcher)
from .common import Common

PERCENT_COLOR = '#AAAAAA'
NAME_LABEL_STYLESHEET = 'font-weight: 600;'

# Mini window
class MiniWindow(QMainWindow):
    def __init__(self, APP_VERSION : str) -> None:
        super().__init__()

        # Settings watcher
        watcher.fileChanged.connect(self.fileChangeEvent)

        # Settings for window
        self.APP_VERSION = APP_VERSION
        self.common = Common()
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
            'lockRatio': Widget(widget = QAction(self),
                                   text = "비율 바 잠금"),
            'changeMode': Widget(widget = QAction(self),
                                 text = "모드 변경"),
            'settings': Widget(widget = QAction(self),
                               text = "설정"),
            'help': Widget(widget = QAction(self),
                           text = "도움말 (공사 중)"),
        }
        self.actions['lockRatio'].getWidget().setCheckable(True)
        self.actions['lockRatio'].getWidget().setChecked(
            True if getPreferences('ratioBarLocked') == 'true' else False)
        self.actions['help'].getWidget().setEnabled(False)

        self.toolsMenu.addAction(self.actions['lockRatio'].getWidget())
        self.toolsMenu.addAction(self.actions['changeMode'].getWidget())
        self.toolsMenu.addSeparator()
        self.toolsMenu.addAction(self.actions['settings'].getWidget())
        self.toolsMenu.addAction(self.actions['help'].getWidget())

        # Ratio box
        self.ratioBox = QGroupBox(self.centralWidget)
        self.ratioBox.setTitle('비율')
        self.ratioBox.setGeometry(QRect(10, 10, 171, 111))
    
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
        self.stuffRatioInputs = [QLineEdit(self.ratioBox), QLineEdit(self.ratioBox), QLineEdit(self.ratioBox)]
        
        for i in range(len(self.stuffRatioInputs)):
            self.stuffRatioInputs[i].setGeometry(QRect(95, (20 + 30 * i), 41, 20))
            self.stuffRatioInputs[i].setAlignment(Qt.AlignRight)
            self.stuffRatioInputs[i].setInputMask('000')
        self.ratioBarButton = Widget(widget = QPushButton(self.centralWidget),
                                     geometry = QRect(10, 130, 171, 31),
                                     text = '비율 바 On / Off')
        
        QMetaObject.connectSlotsByName(self)

        # Actions
        self.actions['changeMode'].getWidget().triggered.connect(self.changeMainDialog)
        self.actions['lockRatio'].getWidget().triggered.connect(self.toggleRatioBarLocked)
        self.actions['settings'].getWidget().triggered.connect(self.common.openSettingsDialog)
        self.ratioBarButton.getWidget().clicked.connect(lambda : self.common.toggleRatioDialog(self.stuffRatioInputs))
        for item in self.stuffRatioInputs:
            item.textChanged.connect(lambda : self.common.updateRatioDialog(self.stuffRatioInputs))

    # Set full ver.
    def setFullWindow(self, window : QWidget) -> None:
        self.full = window

    # Change window
    def changeMainDialog(self) -> None:
        self.full.show()
        self.close()

    # UI elements
    def toggleRatioBarLocked(self) -> None:
        preferences.setValue('ratioBarLocked',
                            self.actions['lockRatio'].getWidget().isChecked())
  
    """ ----------- Events ----------- """
    # If QSettings file has changed
    def fileChangeEvent(self) -> None:
        if self.common.ratioDialog is not None and self.isVisible():
            self.common.updateRatioDialog(self.stuffRatioInputs)

    def closeEvent(self, event : QEvent) -> None:
        if self.common.ratioDialog:
            self.common.ratioDialog.close()
        if self.common.settingsDialog:
            self.common.settingsDialog.close()