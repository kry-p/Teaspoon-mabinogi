# -*- coding: utf-8 -*-
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize,
                            Qt)
from PySide6.QtGui import (QIntValidator)
from PySide6.QtWidgets import (QLabel, QLineEdit, QMainWindow, QPushButton,
                               QRadioButton, QSizePolicy, QTabWidget, QWidget,
                               QMessageBox, QSlider, QColorDialog)
from .preferences_provider import preferences

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

        # 비율 바 옵션
        self.barOption = QWidget()
        self.disclaimerLabel = QLabel(self.barOption)
        self.disclaimerLabel.setGeometry(QRect(40, 0, 240, 20))
        self.disclaimerLabel.setText('※ 변경 사항은 바 On / Off 시 적용됩니다.')

        # 크기
        self.sizeLabel = QLabel(self.barOption)
        self.sizeLabel.setGeometry(QRect(50, 20, 31, 20))
        self.sizeLabelX0 = QLabel(self.barOption)
        self.sizeLabelX0.setGeometry(QRect(148, 20, 16, 20))
        self.ratioBarWidthInput = QLineEdit(self.barOption)
        self.ratioBarWidthInput.setGeometry(QRect(100, 20, 41, 20))
        self.ratioBarWidthInput.setAlignment(Qt.AlignCenter)
        self.ratioBarHeightInput = QLineEdit(self.barOption)
        self.ratioBarHeightInput.setGeometry(QRect(170, 20, 41, 20))
        self.ratioBarHeightInput.setAlignment(Qt.AlignCenter)

        # 위치
        self.positionLabel = QLabel(self.barOption)
        self.positionLabel.setGeometry(QRect(50, 50, 31, 20))
        self.sizeLabelX1 = QLabel(self.barOption)
        self.sizeLabelX1.setGeometry(QRect(148, 50, 16, 20))
        self.ratioBarXPosInput = QLineEdit(self.barOption)
        self.ratioBarXPosInput.setGeometry(QRect(100, 50, 41, 20))
        self.ratioBarXPosInput.setAlignment(Qt.AlignCenter)
        self.ratioBarYPosInput = QLineEdit(self.barOption)
        self.ratioBarYPosInput.setGeometry(QRect(170, 50, 41, 20))
        self.ratioBarYPosInput.setAlignment(Qt.AlignCenter)

        # 색상 A
        self.ratioColorLabel0 = QLabel(self.barOption)
        self.ratioColorLabel0.setGeometry(QRect(50, 80, 41, 20))
        self.ratioColorInput0 = QLineEdit(self.barOption)
        self.ratioColorInput0.setGeometry(QRect(100, 80, 61, 20))
        self.colorSelectButton0 = QPushButton(self.barOption)
        self.colorSelectButton0.setGeometry(QRect(170, 75, 61, 30))

        # 색상 B
        self.ratioColorLabel1 = QLabel(self.barOption)
        self.ratioColorLabel1.setGeometry(QRect(50, 110, 41, 20))
        self.ratioColorInput1 = QLineEdit(self.barOption)
        self.ratioColorInput1.setGeometry(QRect(100, 110, 61, 20))
        self.colorSelectButton1 = QPushButton(self.barOption)
        self.colorSelectButton1.setGeometry(QRect(170, 105, 61, 30))

        # 투명도
        self.opacityLabel = QLabel(self.barOption)
        self.opacityLabel.setGeometry(QRect(50, 140, 41, 20))
        self.opacitySlider = QSlider(self.barOption)
        self.opacitySlider.setGeometry(QRect(100, 140, 131, 22))
        self.opacitySlider.setMaximum(100)
        self.opacitySlider.setOrientation(Qt.Horizontal)

        # 기타 옵션
        self.miscOption = QWidget()

        # 초기 화면
        self.mainWindowLabel = QLabel(self.miscOption)
        self.mainWindowLabel.setGeometry(QRect(30, 20, 61, 20))
        self.mainWindowRadio0 = QRadioButton(self.miscOption)
        self.mainWindowRadio0.setGeometry(QRect(110, 20, 51, 21))
        self.mainWindowRadio1 = QRadioButton(self.miscOption)
        self.mainWindowRadio1.setGeometry(QRect(180, 20, 51, 21))

        # 즐겨찾기 초기화
        self.favResetLabel = QLabel(self.miscOption)
        self.favResetLabel.setGeometry(QRect(30, 60, 61, 31))
        self.resetFavButton = QPushButton(self.miscOption)
        self.resetFavButton.setGeometry(QRect(110, 60, 71, 31))

        # 연락처
        self.supportLabel = QLabel(self.miscOption)
        self.supportLabel.setGeometry(QRect(30, 110, 61, 20))
        self.supportDescLabel = QLabel(self.miscOption)
        self.supportDescLabel.setGeometry(QRect(110, 100, 131, 41))

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
            preferences.value('ratioDialogOpacity')))
        if preferences.value('initialWindowExpanded') == 'true':
            self.mainWindowRadio1.setChecked(True)
        else:
            self.mainWindowRadio0.setChecked(True)

        # 입력값 검증
        self.ratioBarWidthInput.setValidator(QIntValidator(1, 3840))
        self.ratioBarHeightInput.setValidator(QIntValidator(1, 2160))
        self.ratioBarXPosInput.setValidator(QIntValidator(1, 3840))
        self.ratioBarYPosInput.setValidator(QIntValidator(1, 2160))

        # 입력 마스크
        self.ratioColorInput0.setInputMask("\#HHHHHH")
        self.ratioColorInput1.setInputMask("\#HHHHHH")

        # 액션 지정
        self.mainWindowRadio0.clicked.connect(self.onRadioButtonClicked)
        self.mainWindowRadio1.clicked.connect(self.onRadioButtonClicked)
        self.opacitySlider.valueChanged.connect(self.onOpacityChanged)
        self.acceptButton.clicked.connect(self.close)

        self.ratioBarWidthInput.textChanged.connect(self.onXResolutionChanged)
        self.ratioBarHeightInput.textChanged.connect(self.onYResolutionChanged)
        self.ratioBarXPosInput.textChanged.connect(self.onXPositionChanged)
        self.ratioBarYPosInput.textChanged.connect(self.onYPositionChanged)

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
        temp = self.ratioBarWidthInput.text()
        val = preferences.value('ratioDialogSize')

        if temp == '0' or temp == '':
            reply = QMessageBox.critical(
                self, '오류', '너비는 0일 수 없습니다.', QMessageBox.Ok, QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                self.ratioBarWidthInput.setText(str(val['width']))
        else:

            val['width'] = int(self.ratioBarWidthInput.text())
            preferences.setValue('ratioDialogSize', val)

    def onYResolutionChanged(self):
        temp = self.ratioBarHeightInput.text()
        val = preferences.value('ratioDialogSize')

        if temp == '0' or temp == '':
            reply = QMessageBox.critical(
                self, '오류', '높이는 0일 수 없습니다.', QMessageBox.Ok, QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                self.ratioBarHeightInput.setText(str(val['height']))
        else:
            val['height'] = int(self.ratioBarHeightInput.text())
            preferences.setValue('ratioDialogSize', val)

    def onXPositionChanged(self):
        val = preferences.value('ratioDialogDefaultPosition')
        temp = self.ratioBarXPosInput.text()
        if temp == '':
            self.ratioBarXPosInput.setText('0')
        val['x'] = int(self.ratioBarXPosInput.text())
        preferences.setValue('ratioDialogDefaultPosition', val)

    def onYPositionChanged(self):
        val = preferences.value('ratioDialogDefaultPosition')
        val['y'] = int(self.ratioBarYPosInput.text())
        preferences.setValue('ratioDialogDefaultPosition', val)

    def onColor0Changed(self):
        val = preferences.value('ratioBarColor')
        val[0] = self.ratioColorInput0.text()
        preferences.setValue('ratioBarColor', val)

    def onColor1Changed(self):
        val = preferences.value('ratioBarColor')
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
        self.sizeLabel.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">\ud06c\uae30</span></p></body></html>", None))
        self.positionLabel.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">\uc704\uce58</span></p></body></html>", None))

        self.ratioBarWidthInput.setText(
            str(preferences.value('ratioDialogSize')['width']))
        self.ratioBarHeightInput.setText(
            str(preferences.value('ratioDialogSize')['height']))
        self.ratioBarXPosInput.setText(
            str(preferences.value('ratioDialogDefaultPosition')['x']))
        self.ratioBarYPosInput.setText(
            str(preferences.value('ratioDialogDefaultPosition')['y']))
        self.opacityLabel.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">\ud22c\uba85\ub3c4</span></p></body></html>", None))
        self.ratioColorInput0.setText(preferences.value('ratioBarColor')[0])
        self.ratioColorInput1.setText(preferences.value('ratioBarColor')[1])
        self.colorSelectButton0.setText('선택')
        self.colorSelectButton1.setText('선택')

        self.ratioColorLabel1.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">\uc0c9\uc0c1 B</span></p></body></html>", None))
        self.ratioColorLabel0.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">\uc0c9\uc0c1 A</span></p></body></html>", None))
        self.sizeLabelX1.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" color:#aaaaaa;\">x</span></p></body></html>", None))
        self.sizeLabelX0.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" color:#aaaaaa;\">x</span></p></body></html>", None))
        self.settingsWidget.setTabText(self.settingsWidget.indexOf(
            self.barOption), QCoreApplication.translate("MainWindow", u"\ube44\uc728 \ubc14", None))
        self.mainWindowLabel.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">\ucd08\uae30 \ud654\uba74</span></p></body></html>", None))
        self.mainWindowRadio0.setText(QCoreApplication.translate(
            "MainWindow", u"\ubbf8\ub2c8", None))
        self.mainWindowRadio1.setText(QCoreApplication.translate(
            "MainWindow", u"\ud655\uc7a5", None))
        self.favResetLabel.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">\uc990\uaca8\ucc3e\uae30</span></p></body></html>", None))
        self.resetFavButton.setText(QCoreApplication.translate(
            "MainWindow", u"\ucd08\uae30\ud654", None))
        self.supportLabel.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">\uc624\ub958\uc81c\ubcf4</span></p></body></html>", None))
        self.supportDescLabel.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-weight:600; color:#555555;\">\uac8c\uc784 : </span><span style=\" color:#555555;\">[\ud558\ud504] \ub0e5\ud14c</span></p><p><span style=\" font-weight:600; color:#555555;\">\ub514\ucf54 : </span><span style=\" color:#555555;\">Niente#1438</span></p></body></html>", None))
        self.settingsWidget.setTabText(self.settingsWidget.indexOf(
            self.miscOption), QCoreApplication.translate("MainWindow", u"\uae30\ud0c0", None))
        self.acceptButton.setText(QCoreApplication.translate(
            "MainWindow", u"\ud655\uc778", None))
    # retranslateUi
