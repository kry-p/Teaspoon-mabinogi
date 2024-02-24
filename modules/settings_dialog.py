# -*- coding: utf-8 -*-
'''
# Settings window for Spoon
# https://github.com/kry-p/Teaspoon-mabinogi
'''
from PyQt5.QtCore import (QCoreApplication, QMetaObject, QRect, QSize,
                            Qt)
from PyQt5.QtGui import (QIntValidator)
from PyQt5.QtWidgets import (QLabel, QLineEdit, QMainWindow, QPushButton,
                               QRadioButton, QSizePolicy, QTabWidget, QWidget,
                               QMessageBox, QSlider, QColorDialog)
from .preferences_provider import (preferences, watcher, getPreferences)
from .elements import Widget

STYLE_BOLD = 'font-weight: 600;'
WINDOW_WIDTH = 320
WINDOW_HEIGHT = 250

# Settings dialog
class SettingsDialog(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setFixedSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Settings watcher
        watcher.fileChanged.connect(self.onFileChanged)

        # Settings for window
        self.setWindowTitle('설정')

        _sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        _sizePolicy.setHorizontalStretch(0)
        _sizePolicy.setVerticalStretch(0)
        _sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(_sizePolicy)

        self.centralwidget = QWidget(self)
        self.settingsWidget = QTabWidget(self.centralwidget)
        self.settingsWidget.setGeometry(QRect(10, 10, 301, 191))

        self.barOption = QWidget()  # ratio bar
        self.miscOption = QWidget()  # miscellaneous

        # Tabs
        self.settingsWidget.addTab(self.barOption, "")
        self.settingsWidget.addTab(self.miscOption, "")
        
        self.settingsWidget.setTabText(self.settingsWidget.indexOf(self.barOption), '비율 바')
        self.settingsWidget.setTabText(self.settingsWidget.indexOf(self.miscOption), '기타')
        
        # Name labels for settings
        self.nameLabel = {
            'size': Widget(widget = QLabel(self.barOption), geometry = QRect(50, 20, 41, 20), text = '크기', stylesheet = STYLE_BOLD),
            'position': Widget(widget = QLabel(self.barOption), geometry = QRect(50, 50, 41, 20), text = '위치', stylesheet = STYLE_BOLD),
            'colorA': Widget(widget = QLabel(self.barOption), geometry = QRect(50, 80, 41, 20), text = '색상 A', stylesheet = STYLE_BOLD),
            'colorB': Widget(widget = QLabel(self.barOption), geometry = QRect(50, 110, 41, 20), text = '색상 B', stylesheet = STYLE_BOLD),
            'opacity': Widget(widget = QLabel(self.barOption), geometry = QRect(50, 140, 41, 20), text = '투명도', stylesheet = STYLE_BOLD),
            'initialWindow': Widget(widget = QLabel(self.miscOption), geometry = QRect(30, 20, 61, 20), text = '초기 화면', stylesheet = STYLE_BOLD),
            'favorites': Widget(widget = QLabel(self.miscOption), geometry = QRect(30, 60, 61, 20), text = '즐겨찾기', stylesheet = STYLE_BOLD),
            'support': Widget(widget = QLabel(self.miscOption), geometry = QRect(30, 110, 61, 20), text = '오류제보', stylesheet = STYLE_BOLD)
        }
        # Description labels for settings
        self.descLabel = {
            'size': Widget(widget = QLabel(self.barOption), geometry = QRect(148, 20, 16, 20), text = 'x'),
            'position': Widget(widget = QLabel(self.barOption), geometry = QRect(148, 50, 16, 20), text = 'x'),
            'support': Widget(widget = QLabel(self.miscOption), geometry = QRect(110, 100, 131, 41), text = QCoreApplication.translate(
                                                                            "Spoon",
                                                                            u"<html><head/><body><p><span style=\" font-weight:600; color:#555555;\">\
                                                                            \uac8c\uc784 : </span><span style=\" color:#555555;\">[\ud558\ud504] \
                                                                            \ub0e5\ud14c</span></p><p><span style=\" font-weight:600; color:#555555;\">\
                                                                            \ub514\ucf54 : </span><span style=\" color:#555555;\">niente0109</span></p></body></html>",
                                                                            None))}
        # Inputs for ratio bar
        self.input = {
            # size
            'ratioBarWidth': Widget(widget = QLineEdit(self.barOption),
                                    geometry = QRect(100, 20, 41, 20), 
                                    text = str(getPreferences('ratioDialogSize')['width']),
                                    onTextChanged = self.onRatioBarSizeChanged,
                                    validator = QIntValidator(1, 3840)),
            'ratioBarHeight': Widget(widget = QLineEdit(self.barOption),
                                     geometry = QRect(170, 20, 41, 20), 
                                     text = str(getPreferences('ratioDialogSize')['height']),
                                     onTextChanged = self.onRatioBarSizeChanged,
                                     validator = QIntValidator(1, 2160)),
            # position
            'ratioBarXPos': Widget(widget = QLineEdit(self.barOption),
                                   geometry = QRect(100, 50, 41, 20), 
                                   text = str(getPreferences('ratioDialogPosition')['x']),
                                   onTextChanged = self.onRatioBarPositionChanged,
                                   validator = QIntValidator(1, 3840)),
            'ratioBarYPos': Widget(widget = QLineEdit(self.barOption),
                                   geometry = QRect(170, 50, 41, 20), 
                                   text = str(getPreferences('ratioDialogPosition')['y']),
                                   onTextChanged = self.onRatioBarPositionChanged,
                                   validator = QIntValidator(1, 2160)),
            # color
            'ratioBarColor0': Widget(widget = QLineEdit(self.barOption),
                                     geometry = QRect(100, 80, 61, 20), 
                                     text = str(getPreferences('ratioBarColor')[0]),
                                     onTextChanged = self.onColorChanged,
                                     inputMask = ("\#HHHHHH")),
            'ratioBarColor1': Widget(widget = QLineEdit(self.barOption),
                                     geometry = QRect(100, 110, 61, 20), 
                                     text = str(getPreferences('ratioBarColor')[1]),
                                     onTextChanged = self.onColorChanged,
                                     inputMask = ("\#HHHHHH")),
        }
        # Centered text
        for key, item in self.input.items():
            item.getWidget().setAlignment(Qt.AlignCenter)

        # Buttons
        self.button = {
            'colorSelect0': Widget(widget = QPushButton(self.barOption),
                                   geometry = QRect(170, 75, 61, 30),
                                   text = '선택',
                                   onClick = lambda : self.onColorPickerOpened(0)),
            'colorSelect1': Widget(widget = QPushButton(self.barOption),
                                   geometry = QRect(170, 105, 61, 30),
                                   text = '선택',
                                   onClick = lambda : self.onColorPickerOpened(1)),
            'resetFavorites': Widget(widget = QPushButton(self.miscOption),
                                     geometry = QRect(110, 55, 71, 31), 
                                     text = '초기화',
                                     onClick = self.onResetFavorites)
        }

        # Radio group (current main window)
        self.radio = {
            'mainWindowMini': Widget(widget = QRadioButton(self.miscOption),
                                     geometry = QRect(110, 20, 51, 21),
                                     text = '미니',
                                     onClick = self.onRadioButtonClicked),
            'mainWindowFull': Widget(widget = QRadioButton(self.miscOption),
                                     geometry = QRect(180, 20, 51, 21),
                                     text = '확장',
                                     onClick = self.onRadioButtonClicked)
        }

        if getPreferences('initialWindowExpanded') == 'true':
            self.radio['mainWindowFull'].getWidget().setChecked(True)
        else:
            self.radio['mainWindowMini'].getWidget().setChecked(True)

        # Opacity for ratio bar
        self.opacitySlider = QSlider(self.barOption)
        self.opacitySlider.setGeometry(QRect(100, 140, 131, 22))
        self.opacitySlider.setMaximum(101)
        self.opacitySlider.setMinimum(1)
        self.opacitySlider.setOrientation(Qt.Horizontal)

        self.opacitySlider.setSliderPosition(
            int(getPreferences('ratioDialogOpacity')))

        # Dialog button
        self.acceptButton = QPushButton(self.centralwidget)
        self.acceptButton.setGeometry(QRect(115, 210, 91, 32))
        self.acceptButton.setText('확인')
        
        # Misc. actions
        self.opacitySlider.valueChanged.connect(self.onOpacityChanged)
        self.acceptButton.clicked.connect(self.close)

        # Default value
        self.settingsWidget.setCurrentIndex(0)
        self.acceptButton.setDefault(True)

        self.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(self)

    ''' --------------- actions --------------- '''
    def onRadioButtonClicked(self) -> None:
        if self.radio['mainWindowMini'].getWidget().isChecked():
            preferences.setValue('initialWindowExpanded', False)
        else:
            preferences.setValue('initialWindowExpanded', True)

    def onOpacityChanged(self) -> None:
        preferences.setValue('ratioDialogOpacity', self.opacitySlider.value())
    
    def onRatioBarSizeChanged(self) -> None:
        val = getPreferences('ratioDialogSize')
        next = [
            self.input['ratioBarWidth'].getWidget(),
            self.input['ratioBarHeight'].getWidget()
        ]

        for idx in range(len(next)):
            if next[idx].text() == '0' or next[idx].text() == '':
                reply = QMessageBox.critical(
                    self, '오류', '크기는 0일 수 없습니다.', QMessageBox.Ok, QMessageBox.Ok)
                if reply == QMessageBox.Ok:
                    next[idx].setText(str(val['width'])) if idx == 0 else next[idx].setText(str(val['height']))
            else:
                if idx == 0:
                    val['width'] = int(next[idx].text())
                else:
                    val['height'] = int(next[idx].text())
        preferences.setValue('ratioDialogSize', val)

    def onRatioBarPositionChanged(self) -> None:
        val = getPreferences('ratioDialogPosition')
        widget = [self.input['ratioBarXPos'].getWidget(), 
                  self.input['ratioBarYPos'].getWidget()]
        
        for i in range(len(widget)):
            temp = widget[i].text()
            if temp == '':
                widget[i].setText('0')

        val['x'] = int(widget[0].text())
        val['y'] = int(widget[1].text())
    
        preferences.setValue('ratioDialogPosition', val)

    def onColorChanged(self) -> None:
        val = getPreferences('ratioBarColor')
        for i in range(len(val)):
            val[i] = self.input['ratioBarColor%d' % i].getWidget().text()
        preferences.setValue('ratioBarColor', val)
    
    def onColorPickerOpened(self, pos : int) -> None:
        pick = QColorDialog.getColor()
        self.input['ratioBarColor%d' % pos].getWidget().setText(pick.name())

    def onResetFavorites(self) -> None:
        preferences.setValue('favorites', [])

    # If QSettings file has changed
    def onFileChanged(self) -> None:
        # Detects 
        pref = getPreferences('ratioDialogPosition')
        self.input['ratioBarXPos'].getWidget().setText(str(pref['x']))
        self.input['ratioBarYPos'].getWidget().setText(str(pref['y']))