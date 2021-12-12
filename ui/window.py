# -*- coding: utf-8 -*-
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            QSize, Qt, QSettings)
from PySide6.QtGui import (QAction, QCursor, QFont, QIntValidator)
from PySide6.QtWidgets import (QComboBox, QGroupBox, QLabel, QLineEdit,
                               QListView, QMainWindow, QMenu, QMenuBar,
                               QPushButton, QRadioButton, QSizePolicy,
                               QTabWidget, QTextEdit, QWidget, QMessageBox,
                               QSlider, QColorDialog)

defaultSettings = {
    'color': ['#FFFF00', '#FF0000', '#FFFF00'],
    'initialWindowExpanded': True,
    'ratioDialogOpacity': 0,
    'ratioDialogDefaultPosition': {
        'x': 358,
        'y': 690
    },
    'ratioDialogSize': {
        'width': 245,
        'height': 10
    },
    'ratioBarColor': {
        0: '#ffff00',
        1: '#ff0000'
    },
    'favorites': []
}

recipeData = {
    'categories': ['[1] 저미기', '[2] 수비드', '[3] 발효',
                   '[4] 피자 만들기', '[5] 찌기', '[6] 파이 만들기',
                   '[7] 잼 만들기', '[8] 파스타 만들기', '[9] 볶기',
                   '[A] 튀기기', '[B] 면 만들기', '[C] 끓이기',
                   '[D] 반죽', '[E] 삶기', '[F] 굽기',
                   '[P] 혼합', '[N] 기타']
}

rangeFont = QFont('Arial', 1)
settings = QSettings('Yuzu', 'Spoon')

# 비율 바 창


class RatioDialog(QMainWindow):
    def __init__(self, currentValue):
        super().__init__()
        self.currentWindowSize = {
            'width': settings.value('ratioDialogSize')['width'],
            'height': settings.value('ratioDialogSize')['height']
        }
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.move(settings.value('ratioDialogDefaultPosition')['x'],
                  settings.value('ratioDialogDefaultPosition')['y'])

        self.ratio = currentValue
        self.opacity = settings.value('ratioDialogOpacity')

        if not self.opacity:
            settings.setValue('ratioDialogOpacity', 1.0)

        self.initUI()

    # 새로운 값을 계산 후 반영
    def calculate(self):
        list = []
        sum = 0
        temp = 0
        color = settings.value('ratioBarColor')
        for value in self.ratio:
            sum += value

        perValue = self.currentWindowSize['width'] / sum

        for ratioValue in self.ratio:
            if ratioValue == 0:
                continue
            list.append(perValue * ratioValue)

        for i in range(0, len(list)):
            self.labels[i].setGeometry(QRect(temp, 0, temp + list[i], 10))
            self.labels[i].setStyleSheet(
                'background-color: ' + color[i % 2] + ';')

            temp += list[i]

    # 저장된 값을 업데이트
    def update(self, newValue):
        self.ratio = newValue
        self.calculate()

    # UI 요소 초기화
    def initUI(self):
        self.setWindowOpacity(
            1 - float((settings.value('ratioDialogOpacity'))) * 0.008)
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


# 메인 윈도우
class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        # 초기 설정
        for key, value in defaultSettings.items():
            if not settings.contains(key):
                settings.setValue(key, value)

        self._ratioDialog = None
        self._settingsDialog = None
        self._expanded = settings.value('initialWindowExpanded')

        self.setWindow()

        # 메뉴 바 액션
        self.settingsAction = QAction(self)
        self.helpAction = QAction(self)

        # 비율 박스
        self.createStuffBox()

        # 요리 정보 박스
        self.createInfoBox()

        # 왼쪽 툴박스
        self.createLeftToolBox()

        # 기타 버튼
        self.ratioBarButton = QPushButton(self.mainWidget)
        self.ratioBarButton.setGeometry(QRect(10, 280, 171, 31))
        self.expandButton = QPushButton(self.mainWidget)
        self.expandButton.setGeometry(QRect(190, 10, 31, 300))

        self.setCentralWidget(self.mainWidget)
        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 520, 24))
        self.toolsMenu = QMenu(self.menuBar)
        self.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.toolsMenu.menuAction())
        self.toolsMenu.addAction(self.settingsAction)
        self.toolsMenu.addSeparator()
        self.toolsMenu.addAction(self.helpAction)

        self.selectorWidget.setCurrentIndex(0)

        # 비율 초깃값 지정
        self.stuffRatio0.setText('100')
        self.stuffRatio1.setText('100')
        self.stuffRatio2.setText('100')

        # 입력값 검증
        self.stuffRatio0.setInputMask("000")
        self.stuffRatio1.setInputMask("000")
        self.stuffRatio2.setInputMask("000")

        # 액션
        self.ratioBarButton.clicked.connect(self.openCloseRatioDialog)
        self.expandButton.clicked.connect(self.toggleExpandedWindow)
        self.settingsAction.triggered.connect(self.openSettingsDialog)

        # 미구현된 기능 커버
        # for item in recipeData['categories']:
        #     self.rankComboBox.addItem(item)
        self.rankComboBox.addItem("준비중인 기능입니다.")
        self.dummyBox = QPushButton(self.mainWidget)
        self.dummyBox.setText('준비 중인 기능입니다.')
        self.dummyBox.setGeometry(QRect(230, 142, 281, 181))

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    # 창 기본 설정
    def setWindow(self):
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(231, 340))
        self.setMaximumSize(QSize(520, 340))

        if self._expanded == 'true':
            self.resize(520, 340)
            self.setFixedSize(QSize(520, 340))
        else:
            self.resize(231, 340)
            self.setFixedSize(QSize(231, 340))

        self.mainWidget = QWidget(self)

    # 좌측 툴박스
    def createLeftToolBox(self):
        self.selectorWidget = QTabWidget(self.mainWidget)
        self.selectorWidget.setGeometry(QRect(10, 10, 171, 271))

        self.recipeListMenu = QWidget()
        self.searchMenu = QWidget()
        self.favoriteMenu = QWidget()

        # 첫번째 탭
        self.rankComboBox = QComboBox(self.recipeListMenu)
        self.rankComboBox.setGeometry(QRect(12, 10, 141, 22))
        self.recipeListView = QListView(self.recipeListMenu)
        self.recipeListView.setGeometry(QRect(12, 40, 141, 187))

        # 두번째 탭
        self.searchInput = QTextEdit(self.searchMenu)
        self.searchInput.setGeometry(QRect(12, 30, 141, 21))
        self.searchInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.searchInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.searchListView = QListView(self.searchMenu)
        self.searchListView.setGeometry(QRect(12, 56, 141, 171))
        self.nameRadio = QRadioButton(self.searchMenu)
        self.nameRadio.setGeometry(QRect(15, 10, 45, 16))
        self.effectRadio = QRadioButton(self.searchMenu)
        self.effectRadio.setGeometry(QRect(63, 10, 45, 16))
        self.stuffRadio = QRadioButton(self.searchMenu)
        self.stuffRadio.setGeometry(QRect(110, 10, 45, 16))

        # 세번째 탭
        self.favoriteListView = QListView(self.favoriteMenu)
        self.favoriteListView.setGeometry(QRect(12, 10, 141, 195))
        self.alignUpButton = QPushButton(self.favoriteMenu)
        self.alignUpButton.setGeometry(QRect(11, 210, 31, 23))
        self.alignDownButton = QPushButton(self.favoriteMenu)
        self.alignDownButton.setGeometry(QRect(39, 210, 31, 23))
        self.favoriteDeleteButton = QPushButton(self.favoriteMenu)
        self.favoriteDeleteButton.setGeometry(QRect(103, 210, 51, 23))

        self.selectorWidget.addTab(self.recipeListMenu, '')
        self.selectorWidget.addTab(self.searchMenu, '')
        self.selectorWidget.addTab(self.favoriteMenu, '')

    # 비율 박스
    def createStuffBox(self):
        # 비율 입력 박스
        self.ratiobox = QGroupBox(self.mainWidget)
        self.ratiobox.setGeometry(QRect(230, 10, 281, 121))

        self.stuffRatio0 = QLineEdit(self.ratiobox)
        self.stuffRatio0.setGeometry(QRect(200, 30, 41, 20))
        self.stuffLabel1 = QLabel(self.ratiobox)
        self.stuffLabel1.setGeometry(QRect(10, 60, 41, 20))
        self.stuffLabel2 = QLabel(self.ratiobox)
        self.stuffLabel2.setGeometry(QRect(10, 90, 41, 20))

        self.stuffLabel0 = QLabel(self.ratiobox)
        self.stuffLabel0.setGeometry(QRect(10, 30, 41, 20))
        self.stuffRatio1 = QLineEdit(self.ratiobox)
        self.stuffRatio1.setGeometry(QRect(200, 60, 41, 20))
        self.stuffRatio2 = QLineEdit(self.ratiobox)
        self.stuffRatio2.setGeometry(QRect(200, 90, 41, 20))

        self.stuffName0 = QLabel(self.ratiobox)
        self.stuffName0.setGeometry(QRect(60, 30, 121, 20))
        self.stuffName1 = QLabel(self.ratiobox)
        self.stuffName1.setGeometry(QRect(60, 60, 121, 20))
        self.stuffName2 = QLabel(self.ratiobox)
        self.stuffName2.setGeometry(QRect(60, 90, 121, 20))

        self.percentLabel0 = QLabel(self.ratiobox)
        self.percentLabel0.setGeometry(QRect(245, 30, 21, 20))
        self.percentLabel1 = QLabel(self.ratiobox)
        self.percentLabel1.setGeometry(QRect(245, 60, 21, 20))
        self.percentLabel2 = QLabel(self.ratiobox)
        self.percentLabel2.setGeometry(QRect(245, 90, 21, 20))

    # 정보 박스
    def createInfoBox(self):
        self.infoBox = QGroupBox(self.mainWidget)
        self.infoBox.setGeometry(QRect(230, 130, 281, 181))

        self.createChrBox()
        self.createStatBox()
        self.createAtkBox()
        self.createDefBox()

    # HP, MP, SP 박스
    def createChrBox(self):
        self.chrBox = QGroupBox(self.infoBox)
        self.chrBox.setGeometry(QRect(10, 20, 261, 31))

        # 3rd box
        self.hpLabel = QLabel(self.chrBox)
        self.hpLabel.setGeometry(QRect(10, 10, 31, 16))
        self.hpValue = QLabel(self.chrBox)
        self.hpValue.setGeometry(QRect(40, 10, 31, 16))

        self.mpLabel = QLabel(self.chrBox)
        self.mpLabel.setGeometry(QRect(100, 10, 31, 16))
        self.mpValue = QLabel(self.chrBox)
        self.mpValue.setGeometry(QRect(130, 10, 31, 16))

        self.spLabel = QLabel(self.chrBox)
        self.spLabel.setGeometry(QRect(190, 10, 31, 16))
        self.spValue = QLabel(self.chrBox)
        self.spValue.setGeometry(QRect(220, 10, 31, 16))

    # 기초 스테이터스 박스
    def createStatBox(self):
        self.statBox = QGroupBox(self.infoBox)
        self.statBox.setGeometry(QRect(10, 60, 81, 111))

        self.strLabel = QLabel(self.statBox)
        self.strLabel.setGeometry(QRect(10, 10, 31, 16))
        self.strValue = QLabel(self.statBox)
        self.strValue.setGeometry(QRect(40, 10, 31, 16))
        self.intLabel = QLabel(self.statBox)
        self.intLabel.setGeometry(QRect(10, 30, 31, 16))
        self.intValue = QLabel(self.statBox)
        self.intValue.setGeometry(QRect(40, 30, 31, 16))
        self.lucLabel = QLabel(self.statBox)
        self.lucLabel.setGeometry(QRect(10, 90, 31, 16))
        self.lucValue = QLabel(self.statBox)
        self.lucValue.setGeometry(QRect(40, 90, 31, 16))
        self.wilLabel = QLabel(self.statBox)
        self.wilLabel.setGeometry(QRect(10, 70, 31, 16))
        self.wilValue = QLabel(self.statBox)
        self.wilValue.setGeometry(QRect(40, 70, 31, 16))
        self.dexLabel = QLabel(self.statBox)
        self.dexLabel.setGeometry(QRect(10, 50, 31, 16))
        self.dexValue = QLabel(self.statBox)
        self.dexValue.setGeometry(QRect(40, 50, 31, 16))

    # 공격 스테이터스 박스
    def createAtkBox(self):
        self.atkBox = QGroupBox(self.infoBox)
        self.atkBox.setGeometry(QRect(190, 60, 81, 111))

        self.eftLabel = QLabel(self.atkBox)
        self.eftLabel.setGeometry(QRect(10, 90, 31, 16))
        self.eftValue = QLabel(self.atkBox)
        self.eftValue.setGeometry(QRect(40, 90, 31, 16))
        self.mtkLabel = QLabel(self.atkBox)
        self.mtkLabel.setGeometry(QRect(10, 63, 31, 16))
        self.mtkValue = QLabel(self.atkBox)
        self.mtkValue.setGeometry(QRect(40, 63, 31, 16))
        self.minDamLabel = QLabel(self.atkBox)
        self.minDamLabel.setGeometry(QRect(40, 37, 31, 16))
        self.minDamValue = QLabel(self.atkBox)
        self.minDamValue.setGeometry(QRect(40, 10, 31, 16))
        self.maxDamLabel = QLabel(self.atkBox)
        self.maxDamLabel.setGeometry(QRect(10, 10, 31, 16))
        self.maxDamValue = QLabel(self.atkBox)
        self.maxDamValue.setGeometry(QRect(10, 37, 31, 16))

    # 방어 스테이터스 박스
    def createDefBox(self):
        self.defBox = QGroupBox(self.infoBox)
        self.defBox.setGeometry(QRect(100, 60, 81, 111))

        self.mdfLabel = QLabel(self.defBox)
        self.mdfLabel.setGeometry(QRect(10, 63, 31, 16))
        self.mdfValue = QLabel(self.defBox)
        self.mdfValue.setGeometry(QRect(40, 63, 31, 16))
        self.defLabel = QLabel(self.defBox)
        self.defLabel.setGeometry(QRect(10, 10, 31, 16))
        self.defValue = QLabel(self.defBox)
        self.defValue.setGeometry(QRect(40, 10, 31, 16))
        self.mptLabel = QLabel(self.defBox)
        self.mptLabel.setGeometry(QRect(10, 90, 31, 16))
        self.mptValue = QLabel(self.defBox)
        self.mptValue.setGeometry(QRect(40, 90, 31, 16))
        self.prtLabel = QLabel(self.defBox)
        self.prtLabel.setGeometry(QRect(10, 37, 31, 16))
        self.prtValue = QLabel(self.defBox)
        self.prtValue.setGeometry(QRect(40, 37, 31, 16))

    # 메인 창 확장 / 축소
    def toggleExpandedWindow(self):
        if self._expanded:
            self.resize(231, 340)
            self.setFixedSize(QSize(231, 340))
        else:
            self.resize(520, 340)
            self.setFixedSize(QSize(520, 340))
        self._expanded = not self._expanded

    # 설정 창 열기
    def openSettingsDialog(self):
        if self._settingsDialog is None:
            self._settingsDialog = Ui_Settings()
        self._settingsDialog.show()

    # 비율 바 열기 / 닫기
    def openCloseRatioDialog(self):
        data = [
            int(self.stuffRatio0.text()),
            int(self.stuffRatio1.text()),
            int(self.stuffRatio2.text())
        ]
        if self._ratioDialog is None:
            self._ratioDialog = RatioDialog(data)
        else:
            self._ratioDialog.close()
            self._ratioDialog = None

    # 종료 시
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "정말 종료하시겠어요?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self._ratioDialog:
                self._ratioDialog.close()
            if self._settingsDialog:
                self._settingsDialog.close()
            event.accept()
        else:
            event.ignore()

    # 텍스트 지정
    def retranslateUi(self):
        self.setWindowTitle('Spoon v0.1')
        self.settingsAction.setText('설정')
        self.helpAction.setText('도움말')
        self.ratiobox.setTitle('비율')

        # 비율 섹션
        # 재료 라벨
        self.stuffLabel0.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p align=\'center\'><span style=\' font-weight:600;\'>\uc7ac\ub8cc1</span></p></body></html>', None))
        self.stuffLabel1.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p align=\'center\'><span style=\' font-weight:600;\'>\uc7ac\ub8cc2</span></p></body></html>', None))
        self.stuffLabel2.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p align=\'center\'><span style=\' font-weight:600;\'>\uc7ac\ub8cc3</span></p></body></html>', None))

        # 재료 이름 라벨
        self.stuffName0.setText('')
        self.stuffName1.setText('')
        self.stuffName2.setText('')

        # % 기호 라벨
        self.percentLabel0.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' color:#aaaaaa;\'>%</span></p></body></html>', None))
        self.percentLabel1.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' color:#aaaaaa;\'>%</span></p></body></html>', None))
        self.percentLabel2.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' color:#aaaaaa;\'>%</span></p></body></html>', None))

        self.infoBox.setTitle(QCoreApplication.translate(
            'Spoon', u'\uc815\ubcf4', None))
        self.chrBox.setTitle('')
        self.statBox.setTitle('')
        self.defBox.setTitle('')
        self.atkBox.setTitle('')

        self.hpLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>HP</span></p></body></html>', None))
        self.mpLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>MP</span></p></body></html>', None))
        self.hpValue.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p>r_K</p></body></html>', None))
        self.spLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>SP</span></p></body></html>', None))
        self.mpValue.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p>r_L</p></body></html>', None))
        self.spValue.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p>r_M</p></body></html>', None))

        self.strValue.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p>r_F</p></body></html>', None))
        self.strLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\uccb4\ub825</span></p></body></html>', None))
        self.intValue.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p>r_G</p></body></html>', None))
        self.lucValue.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p>r_J</p></body></html>', None))
        self.lucLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ud589\uc6b4</span></p></body></html>', None))
        self.intLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\uc9c0\ub825</span></p></body></html>', None))
        self.wilLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\uc758\uc9c0</span></p></body></html>', None))
        self.wilValue.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p>r_I</p></body></html>', None))
        self.dexLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\uc19c\uc528</span></p></body></html>', None))
        self.dexValue.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p>r_H</p></body></html>', None))

        self.mdfLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ub9c8\ubc29</span></p></body></html>', None))
        self.defLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ubc29\uc5b4</span></p></body></html>', None))
        self.mptLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ub9c8\ubcf4</span></p></body></html>', None))
        self.defValue.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p>r_Q</p></body></html>', None))
        self.prtLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ubcf4\ud638</span></p></body></html>', None))
        self.mptValue.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p>r_T</p></body></html>', None))
        self.prtValue.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p>r_R</p></body></html>', None))
        self.mdfValue.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p>r_S</p></body></html>', None))

        self.eftValue.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p>r_U</p></body></html>', None))
        self.mtkValue.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p>r_P</p></body></html>', None))
        self.eftLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ud6a8\uacfc</span></p></body></html>', None))
        self.minDamValue.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p>r_N</p></body></html>', None))
        self.maxDamValue.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ub9e5\ub310</span></p></body></html>', None))
        self.maxDamLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ubbfc\ub310</span></p></body></html>', None))
        self.minDamLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p>r_O</p></body></html>', None))
        self.mtkLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ub9c8\uacf5</span></p></body></html>', None))
        self.selectorWidget.setTabText(self.selectorWidget.indexOf(
            self.recipeListMenu), QCoreApplication.translate('Spoon', u'\ubaa9\ub85d', None))
        self.nameRadio.setText(QCoreApplication.translate(
            'Spoon', u'\uc774\ub984', None))
        self.effectRadio.setText(QCoreApplication.translate(
            'Spoon', u'\ud6a8\uacfc', None))
        self.stuffRadio.setText(QCoreApplication.translate(
            'Spoon', u'\uc7ac\ub8cc', None))
        self.selectorWidget.setTabText(self.selectorWidget.indexOf(
            self.searchMenu), QCoreApplication.translate('Spoon', u'\uac80\uc0c9', None))

        self.alignUpButton.setText(
            QCoreApplication.translate('Spoon', u'\u25b3', None))
        self.alignDownButton.setText(
            QCoreApplication.translate('Spoon', u'\u25bd', None))
        self.favoriteDeleteButton.setText(
            QCoreApplication.translate('Spoon', u'\uc0ad\uc81c', None))

        self.selectorWidget.setTabText(self.selectorWidget.indexOf(
            self.favoriteMenu), QCoreApplication.translate('Spoon', u'\u2606', None))
        self.ratioBarButton.setText(QCoreApplication.translate(
            'Spoon', u'\ube44\uc728 \ubc14 On / Off', None))
        self.expandButton.setText(
            QCoreApplication.translate('Spoon', u'\u300b', None))
        self.toolsMenu.setTitle(QCoreApplication.translate(
            'Spoon', u'\ub3c4\uad6c', None))

# 설정 창


class Ui_Settings(QMainWindow):
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
            settings.value('ratioDialogOpacity')))
        if settings.value('initialWindowExpanded') == 'true':
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
            settings.setValue('initialWindowExpanded', False)
        else:
            settings.setValue('initialWindowExpanded', True)

    def onOpacityChanged(self):
        settings.setValue('ratioDialogOpacity', self.opacitySlider.value())

    def onXResolutionChanged(self):
        temp = self.ratioBarWidthInput.text()
        val = settings.value('ratioDialogSize')

        if temp == '0' or temp == '':
            reply = QMessageBox.critical(
                self, '오류', '너비는 0일 수 없습니다.', QMessageBox.Ok, QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                self.ratioBarWidthInput.setText(str(val['width']))
        else:

            val['width'] = int(self.ratioBarWidthInput.text())
            settings.setValue('ratioDialogSize', val)

    def onYResolutionChanged(self):
        temp = self.ratioBarHeightInput.text()
        val = settings.value('ratioDialogSize')

        if temp == '0' or temp == '':
            reply = QMessageBox.critical(
                self, '오류', '높이는 0일 수 없습니다.', QMessageBox.Ok, QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                self.ratioBarHeightInput.setText(str(val['height']))
        else:
            val['height'] = int(self.ratioBarHeightInput.text())
            settings.setValue('ratioDialogSize', val)

    def onXPositionChanged(self):
        val = settings.value('ratioDialogDefaultPosition')
        temp = self.ratioBarXPosInput.text()
        if temp == '':
            self.ratioBarXPosInput.setText('0')
        val['x'] = int(self.ratioBarXPosInput.text())
        settings.setValue('ratioDialogDefaultPosition', val)

    def onYPositionChanged(self):
        val = settings.value('ratioDialogDefaultPosition')
        val['y'] = int(self.ratioBarYPosInput.text())
        settings.setValue('ratioDialogDefaultPosition', val)

    def onColor0Changed(self):
        val = settings.value('ratioBarColor')
        val[0] = self.ratioColorInput0.text()
        settings.setValue('ratioBarColor', val)

    def onColor1Changed(self):
        val = settings.value('ratioBarColor')
        val[1] = self.ratioColorInput1.text()
        settings.setValue('ratioBarColor', val)

    def onResetFavorites(self):
        settings.setValue('favorites', [])

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
            str(settings.value('ratioDialogSize')['width']))
        self.ratioBarHeightInput.setText(
            str(settings.value('ratioDialogSize')['height']))
        self.ratioBarXPosInput.setText(
            str(settings.value('ratioDialogDefaultPosition')['x']))
        self.ratioBarYPosInput.setText(
            str(settings.value('ratioDialogDefaultPosition')['y']))
        self.opacityLabel.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">\ud22c\uba85\ub3c4</span></p></body></html>", None))
        self.ratioColorInput0.setText(settings.value('ratioBarColor')[0])
        self.ratioColorInput1.setText(settings.value('ratioBarColor')[1])
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
