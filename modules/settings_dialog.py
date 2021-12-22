# -*- coding: utf-8 -*-
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize,
                            Qt)
from PySide6.QtGui import (QIntValidator)
from PySide6.QtWidgets import (QLabel, QLineEdit, QMainWindow, QPushButton,
                               QRadioButton, QSizePolicy, QTabWidget, QWidget,
                               QMessageBox, QSlider, QColorDialog)
from .preferences_provider import preferences, getPreferences
from .elements import Label, LineEdit

STYLE_BOLD = 'font-weight: 600;'

# 설정 창
class SettingsDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(320, 250)
        self.setFixedSize(QSize(320, 250))

        # 창 설정
        _sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        _sizePolicy.setHorizontalStretch(0)
        _sizePolicy.setVerticalStretch(0)
        _sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(_sizePolicy)

        self.centralwidget = QWidget(self)
        self.settingsWidget = QTabWidget(self.centralwidget)
        self.settingsWidget.setGeometry(QRect(10, 10, 301, 191))

        self.barOption = QWidget()  # 비율 바 옵션
        self.miscOption = QWidget()  # 기타 옵션

        # 설정 이름 라벨
        self.nameLabel = {
            'size': Label(QLabel(self.barOption), QRect(50, 20, 41, 20), '크기'),
            'position': Label(QLabel(self.barOption), QRect(50, 50, 41, 20), '위치'),
            'colorA': Label(QLabel(self.barOption), QRect(50, 80, 41, 20), '색상 A'),
            'colorB': Label(QLabel(self.barOption), QRect(50, 110, 41, 20), '색상 B'),
            'opacity': Label(QLabel(self.barOption), QRect(50, 140, 41, 20), '투명도'),
            'initialWindow': Label(QLabel(self.miscOption), QRect(30, 20, 61, 20), '초기 화면'),
            'favorites': Label(QLabel(self.miscOption), QRect(30, 60, 61, 20), '즐겨찾기'),
            'support': Label(QLabel(self.miscOption), QRect(30, 110, 61, 20), '오류제보')
        }

        for key, item in self.nameLabel.items():
            item.setStyle(STYLE_BOLD)

        # 내용 라벨
        self.descLabel = {
            'size': Label(QLabel(self.barOption), QRect(148, 20, 16, 20), 'x'),
            'position': Label(QLabel(self.barOption), QRect(148, 50, 16, 20), 'x'),
            'support': Label(QLabel(self.miscOption), QRect(110, 100, 131, 41), QCoreApplication.translate(
                                                                            "MainWindow",
                                                                            u"<html><head/><body><p><span style=\" font-weight:600; color:#555555;\">\
                                                                            \uac8c\uc784 : </span><span style=\" color:#555555;\">[\ud558\ud504] \
                                                                            \ub0e5\ud14c</span></p><p><span style=\" font-weight:600; color:#555555;\">\
                                                                            \ub514\ucf54 : </span><span style=\" color:#555555;\">Niente#1438</span></p></body></html>",
                                                                            None))}

        # 입력
        self.input = {
            'ratioBarWidth': LineEdit(QLineEdit(self.barOption),
                                      QRect(100, 20, 41, 20), 
                                      str(getPreferences('ratioDialogSize')['width'])),
            'ratioBarHeight': LineEdit(QLineEdit(self.barOption),
                                       QRect(170, 20, 41, 20), 
                                       str(getPreferences('ratioDialogSize')['height'])),
            'ratioBarXPos': LineEdit(QLineEdit(self.barOption),
                                     QRect(100, 50, 41, 20), 
                                     str(getPreferences('ratioDialogDefaultPosition')['x'])),
            'ratioBarYPos': LineEdit(QLineEdit(self.barOption),
                                     QRect(170, 50, 41, 20), 
                                     str(getPreferences('ratioDialogDefaultPosition')['y'])),
        }
        for key, item in self.input.items():
            item.getInput().setAlignment(Qt.AlignCenter)

        self.input['ratioBarWidth'].setTextChangedAction(self.onXResolutionChanged)
        self.input['ratioBarHeight'].setTextChangedAction(self.onYResolutionChanged)
        self.input['ratioBarXPos'].setTextChangedAction(self.onXPositionChanged)
        self.input['ratioBarYPos'].setTextChangedAction(self.onYPositionChanged)

        # 색상 A
        self.ratioColorInput0 = QLineEdit(self.barOption)
        self.ratioColorInput0.setGeometry(QRect(100, 80, 61, 20))
        self.colorSelectButton0 = QPushButton(self.barOption)
        self.colorSelectButton0.setGeometry(QRect(170, 75, 61, 30))

        # 색상 B
        self.ratioColorInput1 = QLineEdit(self.barOption)
        self.ratioColorInput1.setGeometry(QRect(100, 110, 61, 20))
        self.colorSelectButton1 = QPushButton(self.barOption)
        self.colorSelectButton1.setGeometry(QRect(170, 105, 61, 30))

        # 투명도
        self.opacitySlider = QSlider(self.barOption)
        self.opacitySlider.setGeometry(QRect(100, 140, 131, 22))
        self.opacitySlider.setMaximum(100)
        self.opacitySlider.setOrientation(Qt.Horizontal)

        # 초기 화면
        self.mainWindowRadio0 = QRadioButton(self.miscOption)
        self.mainWindowRadio0.setGeometry(QRect(110, 20, 51, 21))
        self.mainWindowRadio1 = QRadioButton(self.miscOption)
        self.mainWindowRadio1.setGeometry(QRect(180, 20, 51, 21))

        # 즐겨찾기 초기화
        self.resetFavButton = QPushButton(self.miscOption)
        self.resetFavButton.setGeometry(QRect(110, 60, 71, 31))

        # 연락처

        # Dialog 버튼
        self.acceptButton = QPushButton(self.centralwidget)
        self.acceptButton.setGeometry(QRect(115, 210, 91, 32))

        self.settingsWidget.addTab(self.barOption, "")
        self.settingsWidget.addTab(self.miscOption, "")

        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()

        # 초깃값 지정
        self.settingsWidget.setCurrentIndex(0)
        self.acceptButton.setDefault(True)

        QMetaObject.connectSlotsByName(self)

        # 설정에서 초깃값 지정
        self.opacitySlider.setSliderPosition(float(
            getPreferences('ratioDialogOpacity')))
        if getPreferences('initialWindowExpanded') == 'true':
            self.mainWindowRadio1.setChecked(True)
        else:
            self.mainWindowRadio0.setChecked(True)

        # 입력값 검증
        self.input['ratioBarWidth'].setValidator(QIntValidator(1, 3840))
        self.input['ratioBarHeight'].setValidator(QIntValidator(1, 2160))
        self.input['ratioBarXPos'].setValidator(QIntValidator(1, 3840))
        self.input['ratioBarYPos'].setValidator(QIntValidator(1, 2160))

        # 입력 마스크
        self.ratioColorInput0.setInputMask("\#HHHHHH")
        self.ratioColorInput1.setInputMask("\#HHHHHH")

        # 액션 지정
        self.mainWindowRadio0.clicked.connect(self.onRadioButtonClicked)
        self.mainWindowRadio1.clicked.connect(self.onRadioButtonClicked)
        self.opacitySlider.valueChanged.connect(self.onOpacityChanged)
        self.acceptButton.clicked.connect(self.close)

        self.ratioColorInput0.textChanged.connect(self.onColor0Changed)
        self.ratioColorInput1.textChanged.connect(self.onColor1Changed)

        self.colorSelectButton0.clicked.connect(self.onColorPicker0Opened)
        self.colorSelectButton1.clicked.connect(self.onColorPicker1Opened)

        self.resetFavButton.clicked.connect(self.onResetFavorites)

    def onRadioButtonClicked(self):
        if self.mainWindowRadio0.isChecked():
            preferences.setValue('initialWindowExpanded', False)
        else:
            preferences.setValue('initialWindowExpanded', True)

    def onOpacityChanged(self):
        preferences.setValue('ratioDialogOpacity', self.opacitySlider.value())

    def onXResolutionChanged(self):
        temp = self.input['ratioBarWidth'].getText()
        val = getPreferences('ratioDialogSize')

        if temp == '0' or temp == '':
            reply = QMessageBox.critical(
                self, '오류', '너비는 0일 수 없습니다.', QMessageBox.Ok, QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                self.input['ratioBarWidth'].setText(str(val['width']))
        else:
            val['width'] = int(self.input['ratioBarWidth'].getText())
            preferences.setValue('ratioDialogSize', val)

    def onYResolutionChanged(self):
        temp = self.input['ratioBarHeight'].getText()
        val = getPreferences('ratioDialogSize')

        if temp == '0' or temp == '':
            reply = QMessageBox.critical(
                self, '오류', '높이는 0일 수 없습니다.', QMessageBox.Ok, QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                self.input['ratioBarHeight'].setText(str(val['height']))
        else:
            val['height'] = int(self.input['ratioBarHeight'].getText())
            preferences.setValue('ratioDialogSize', val)

    def onXPositionChanged(self):
        val = getPreferences('ratioDialogDefaultPosition')
        temp = self.input['ratioBarXPos'].getText()
        if temp == '':
            self.input['ratioBarXPos'].setText('0')
        val['x'] = int(self.input['ratioBarXPos'].getText())
        preferences.setValue('ratioDialogDefaultPosition', val)

    def onYPositionChanged(self):
        val = getPreferences('ratioDialogDefaultPosition')
        temp = self.input['ratioBarYPos'].getText()
        if temp == '':
            self.input['ratioBarYPos'].setText('0')
        val['y'] = int(self.input['ratioBarYPos'].getText())
        preferences.setValue('ratioDialogDefaultPosition', val)

    def onColor0Changed(self):
        val = getPreferences('ratioBarColor')
        val[0] = self.ratioColorInput0.text()
        preferences.setValue('ratioBarColor', val)

    def onColor1Changed(self):
        val = getPreferences('ratioBarColor')
        val[1] = self.ratioColorInput1.text()
        preferences.setValue('ratioBarColor', val)

    def onResetFavorites(self):
        preferences.setValue('favorites', [])

    def onColorPicker0Opened(self):
        pick = QColorDialog.getColor()
        self.ratioColorInput0.setText(pick.name())

    def onColorPicker1Opened(self):
        pick = QColorDialog.getColor()
        self.ratioColorInput1.setText(pick.name())

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"\uc124\uc815", None))

        self.ratioColorInput0.setText(getPreferences('ratioBarColor')[0])
        self.ratioColorInput1.setText(getPreferences('ratioBarColor')[1])
        self.colorSelectButton0.setText('선택')
        self.colorSelectButton1.setText('선택')

        self.settingsWidget.setTabText(self.settingsWidget.indexOf(
            self.barOption), QCoreApplication.translate("MainWindow", u"\ube44\uc728 \ubc14", None))

        self.mainWindowRadio0.setText(QCoreApplication.translate(
            "MainWindow", u"\ubbf8\ub2c8", None))
        self.mainWindowRadio1.setText(QCoreApplication.translate(
            "MainWindow", u"\ud655\uc7a5", None))
        self.resetFavButton.setText(QCoreApplication.translate(
            "MainWindow", u"\ucd08\uae30\ud654", None))
        self.settingsWidget.setTabText(self.settingsWidget.indexOf(
            self.miscOption), QCoreApplication.translate("MainWindow", u"\uae30\ud0c0", None))
        self.acceptButton.setText(QCoreApplication.translate(
            "MainWindow", u"\ud655\uc778", None))
