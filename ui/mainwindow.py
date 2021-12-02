# -*- coding: utf-8 -*-
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
                           QCursor, QFont, QFontDatabase, QGradient,
                           QIcon, QImage, QKeySequence, QLinearGradient,
                           QPainter, QPalette, QPixmap, QRadialGradient,
                           QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QLabel,
                               QLineEdit, QListView, QMainWindow, QMenu,
                               QMenuBar, QPushButton, QRadioButton, QSizePolicy,
                               QTabWidget, QTextEdit, QWidget)

settings = {
    'color': ['#FFFF00', '#FF0000', '#FFFF00'],
    'transparency': 0
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


# 비율 바 창
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
            self.labels[i].setStyleSheet(
                "background-color: " + settings['color'][i] + ";")

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


# 메인 윈도우
class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        # 창 설정
        self._ratioDialog = None
        self._expanded = False

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(231, 340))
        self.setMaximumSize(QSize(520, 340))

        if self._expanded:
            self.resize(520, 340)
            self.setFixedSize(QSize(520, 340))
        else:
            self.resize(231, 340)
            self.setFixedSize(QSize(231, 340))

        self.mainWidget = QWidget(self)
        self.mainWidget.setObjectName(u"mainWidget")

        # 메뉴 바 액션
        self.settingsAction = QAction(self)
        self.settingsAction.setObjectName(u"settingsAction")
        self.helpAction = QAction(self)
        self.helpAction.setObjectName(u"helpAction")

        # 비율 입력 박스
        self.ratiobox = QGroupBox(self.mainWidget)
        self.ratiobox.setObjectName(u"ratiobox")
        self.ratiobox.setGeometry(QRect(230, 10, 281, 121))
        self.stuffLabel1 = QLabel(self.ratiobox)
        self.stuffLabel1.setObjectName(u"stuffLabel1")
        self.stuffLabel1.setGeometry(QRect(10, 60, 41, 20))
        self.stuffLabel2 = QLabel(self.ratiobox)
        self.stuffLabel2.setObjectName(u"stuffLabel2")
        self.stuffLabel2.setGeometry(QRect(10, 90, 41, 20))
        self.stuffRatio0 = QLineEdit(self.ratiobox)
        self.stuffRatio0.setObjectName(u"stuffRatio0")
        self.stuffRatio0.setGeometry(QRect(200, 30, 41, 20))
        self.stuffRatio1 = QLineEdit(self.ratiobox)
        self.stuffRatio1.setObjectName(u"stuffRatio1")
        self.stuffRatio1.setGeometry(QRect(200, 60, 41, 20))
        self.stuffLabel0 = QLabel(self.ratiobox)
        self.stuffLabel0.setObjectName(u"stuffLabel0")
        self.stuffLabel0.setGeometry(QRect(10, 30, 41, 20))
        self.stuffRatio2 = QLineEdit(self.ratiobox)
        self.stuffRatio2.setObjectName(u"stuffRatio2")
        self.stuffRatio2.setGeometry(QRect(200, 90, 41, 20))
        self.stuffName0 = QLabel(self.ratiobox)
        self.stuffName0.setObjectName(u"stuffName0")
        self.stuffName0.setGeometry(QRect(60, 30, 121, 20))
        self.stuffName1 = QLabel(self.ratiobox)
        self.stuffName1.setObjectName(u"stuffName1")
        self.stuffName1.setGeometry(QRect(60, 60, 121, 20))
        self.stuffName2 = QLabel(self.ratiobox)
        self.stuffName2.setObjectName(u"stuffName2")
        self.stuffName2.setGeometry(QRect(60, 90, 121, 20))
        self.percentLabel1 = QLabel(self.ratiobox)
        self.percentLabel1.setObjectName(u"percentLabel1")
        self.percentLabel1.setGeometry(QRect(245, 60, 21, 20))
        self.percentLabel2 = QLabel(self.ratiobox)
        self.percentLabel2.setObjectName(u"percentLabel2")
        self.percentLabel2.setGeometry(QRect(245, 90, 21, 20))
        self.percentLabel0 = QLabel(self.ratiobox)
        self.percentLabel0.setObjectName(u"percentLabel0")
        self.percentLabel0.setGeometry(QRect(245, 30, 21, 20))

        self.stuffRatio0.setText('100')
        self.stuffRatio1.setText('100')
        self.stuffRatio2.setText('100')

        # 요리 정보 박스
        self.infoBox = QGroupBox(self.mainWidget)
        self.infoBox.setObjectName(u"infoBox")
        self.infoBox.setGeometry(QRect(230, 130, 281, 181))

        self.chrBox = QGroupBox(self.infoBox)
        self.chrBox.setObjectName(u"chrBox")
        self.chrBox.setGeometry(QRect(10, 20, 261, 31))

        self.statBox = QGroupBox(self.infoBox)
        self.statBox.setObjectName(u"statBox")
        self.statBox.setGeometry(QRect(10, 60, 81, 111))

        self.defBox = QGroupBox(self.infoBox)
        self.defBox.setObjectName(u"defBox")
        self.defBox.setGeometry(QRect(100, 60, 81, 111))

        self.atkBox = QGroupBox(self.infoBox)
        self.atkBox.setObjectName(u"atkBox")
        self.atkBox.setGeometry(QRect(190, 60, 81, 111))

        # 3rd box
        self.hpLabel = QLabel(self.chrBox)
        self.hpLabel.setObjectName(u"hpLabel")
        self.hpLabel.setGeometry(QRect(10, 10, 31, 16))
        self.hpValue = QLabel(self.chrBox)
        self.hpValue.setObjectName(u"hpValue")
        self.hpValue.setGeometry(QRect(40, 10, 31, 16))

        self.mpLabel = QLabel(self.chrBox)
        self.mpLabel.setObjectName(u"mpLabel")
        self.mpLabel.setGeometry(QRect(100, 10, 31, 16))
        self.mpValue = QLabel(self.chrBox)
        self.mpValue.setObjectName(u"mpValue")
        self.mpValue.setGeometry(QRect(130, 10, 31, 16))

        self.spLabel = QLabel(self.chrBox)
        self.spLabel.setObjectName(u"spLabel")
        self.spLabel.setGeometry(QRect(190, 10, 31, 16))
        self.spValue = QLabel(self.chrBox)
        self.spValue.setObjectName(u"spValue")
        self.spValue.setGeometry(QRect(220, 10, 31, 16))

        # 4th box
        self.strLabel = QLabel(self.statBox)
        self.strLabel.setObjectName(u"strLabel")
        self.strLabel.setGeometry(QRect(10, 10, 31, 16))
        self.strValue = QLabel(self.statBox)
        self.strValue.setObjectName(u"strValue")
        self.strValue.setGeometry(QRect(40, 10, 31, 16))

        self.intLabel = QLabel(self.statBox)
        self.intLabel.setObjectName(u"intLabel")
        self.intLabel.setGeometry(QRect(10, 30, 31, 16))
        self.intValue = QLabel(self.statBox)
        self.intValue.setObjectName(u"intValue")
        self.intValue.setGeometry(QRect(40, 30, 31, 16))

        self.lucLabel = QLabel(self.statBox)
        self.lucLabel.setObjectName(u"lucLabel")
        self.lucLabel.setGeometry(QRect(10, 90, 31, 16))
        self.lucValue = QLabel(self.statBox)
        self.lucValue.setObjectName(u"lucValue")
        self.lucValue.setGeometry(QRect(40, 90, 31, 16))

        self.wilLabel = QLabel(self.statBox)
        self.wilLabel.setObjectName(u"wilLabel")
        self.wilLabel.setGeometry(QRect(10, 70, 31, 16))
        self.wilValue = QLabel(self.statBox)
        self.wilValue.setObjectName(u"wilValue")
        self.wilValue.setGeometry(QRect(40, 70, 31, 16))

        self.dexLabel = QLabel(self.statBox)
        self.dexLabel.setObjectName(u"dexLabel")
        self.dexLabel.setGeometry(QRect(10, 50, 31, 16))
        self.dexValue = QLabel(self.statBox)
        self.dexValue.setObjectName(u"dexValue")
        self.dexValue.setGeometry(QRect(40, 50, 31, 16))

        # 5th box
        self.mdfLabel = QLabel(self.defBox)
        self.mdfLabel.setObjectName(u"mdfLabel")
        self.mdfLabel.setGeometry(QRect(10, 63, 31, 16))
        self.mdfValue = QLabel(self.defBox)
        self.mdfValue.setObjectName(u"mdfValue")
        self.mdfValue.setGeometry(QRect(40, 63, 31, 16))

        self.defLabel = QLabel(self.defBox)
        self.defLabel.setObjectName(u"defLabel")
        self.defLabel.setGeometry(QRect(10, 10, 31, 16))
        self.defValue = QLabel(self.defBox)
        self.defValue.setObjectName(u"defValue")
        self.defValue.setGeometry(QRect(40, 10, 31, 16))

        self.mptLabel = QLabel(self.defBox)
        self.mptLabel.setObjectName(u"mptLabel")
        self.mptLabel.setGeometry(QRect(10, 90, 31, 16))
        self.mptValue = QLabel(self.defBox)
        self.mptValue.setObjectName(u"mptValue")
        self.mptValue.setGeometry(QRect(40, 90, 31, 16))

        self.prtLabel = QLabel(self.defBox)
        self.prtLabel.setObjectName(u"prtLabel")
        self.prtLabel.setGeometry(QRect(10, 37, 31, 16))
        self.prtValue = QLabel(self.defBox)
        self.prtValue.setObjectName(u"prtValue")
        self.prtValue.setGeometry(QRect(40, 37, 31, 16))

        # 6th box
        self.eftLabel = QLabel(self.atkBox)
        self.eftLabel.setObjectName(u"eftLabel")
        self.eftLabel.setGeometry(QRect(10, 90, 31, 16))
        self.eftValue = QLabel(self.atkBox)
        self.eftValue.setObjectName(u"eftValue")
        self.eftValue.setGeometry(QRect(40, 90, 31, 16))

        self.mtkLabel = QLabel(self.atkBox)
        self.mtkLabel.setObjectName(u"mtkLabel")
        self.mtkLabel.setGeometry(QRect(10, 63, 31, 16))
        self.mtkValue = QLabel(self.atkBox)
        self.mtkValue.setObjectName(u"mtkValue")
        self.mtkValue.setGeometry(QRect(40, 63, 31, 16))

        self.minDamLabel = QLabel(self.atkBox)
        self.minDamLabel.setObjectName(u"minDamLabel")
        self.minDamLabel.setGeometry(QRect(40, 37, 31, 16))
        self.minDamValue = QLabel(self.atkBox)
        self.minDamValue.setObjectName(u"minDamValue")
        self.minDamValue.setGeometry(QRect(40, 10, 31, 16))

        self.maxDamLabel = QLabel(self.atkBox)
        self.maxDamLabel.setObjectName(u"maxDamLabel")
        self.maxDamLabel.setGeometry(QRect(10, 10, 31, 16))
        self.maxDamValue = QLabel(self.atkBox)
        self.maxDamValue.setObjectName(u"maxDamValue")
        self.maxDamValue.setGeometry(QRect(10, 37, 31, 16))

        # Left tab
        self.selectorWidget = QTabWidget(self.mainWidget)
        self.selectorWidget.setObjectName(u"selectorWidget")
        self.selectorWidget.setGeometry(QRect(10, 10, 171, 271))

        # Left menu
        self.recipeListMenu = QWidget()
        self.recipeListMenu.setObjectName(u"recipeListMenu")

        self.searchMenu = QWidget()
        self.searchMenu.setObjectName(u"searchMenu")

        self.favoriteMenu = QWidget()
        self.favoriteMenu.setObjectName(u"favoriteMenu")

        # First left menu
        self.rankComboBox = QComboBox(self.recipeListMenu)
        self.rankComboBox.setObjectName(u"rankComboBox")
        self.rankComboBox.setGeometry(QRect(12, 10, 141, 22))
        self.recipeListView = QListView(self.recipeListMenu)
        self.recipeListView.setObjectName(u"recipeListView")
        self.recipeListView.setGeometry(QRect(12, 40, 141, 187))

        self.searchInput = QTextEdit(self.searchMenu)
        self.searchInput.setObjectName(u"searchInput")
        self.searchInput.setGeometry(QRect(12, 30, 141, 21))
        self.searchInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.searchInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.searchListView = QListView(self.searchMenu)
        self.searchListView.setObjectName(u"searchListView")
        self.searchListView.setGeometry(QRect(12, 56, 141, 171))
        self.nameRadio = QRadioButton(self.searchMenu)
        self.nameRadio.setObjectName(u"nameRadio")
        self.nameRadio.setGeometry(QRect(15, 10, 45, 16))
        self.effectRadio = QRadioButton(self.searchMenu)
        self.effectRadio.setObjectName(u"effectRadio")
        self.effectRadio.setGeometry(QRect(63, 10, 45, 16))
        self.stuffRadio = QRadioButton(self.searchMenu)
        self.stuffRadio.setObjectName(u"stuffRadio")
        self.stuffRadio.setGeometry(QRect(110, 10, 45, 16))

        self.favoriteListView = QListView(self.favoriteMenu)
        self.favoriteListView.setObjectName(u"favoriteListView")
        self.favoriteListView.setGeometry(QRect(12, 10, 141, 195))
        self.alignUpButton = QPushButton(self.favoriteMenu)
        self.alignUpButton.setObjectName(u"alignUpButton")
        self.alignUpButton.setGeometry(QRect(11, 210, 31, 23))
        self.alignDownButton = QPushButton(self.favoriteMenu)
        self.alignDownButton.setObjectName(u"alignDownButton")
        self.alignDownButton.setGeometry(QRect(39, 210, 31, 23))
        self.favoriteDeleteButton = QPushButton(self.favoriteMenu)
        self.favoriteDeleteButton.setObjectName(u"favoriteDeleteButton")
        self.favoriteDeleteButton.setGeometry(QRect(103, 210, 51, 23))

        self.selectorWidget.addTab(self.recipeListMenu, "")
        self.selectorWidget.addTab(self.searchMenu, "")
        self.selectorWidget.addTab(self.favoriteMenu, "")

        # Misc. buttons
        self.ratioBarButton = QPushButton(self.mainWidget)
        self.ratioBarButton.setObjectName(u"ratioBarButton")
        self.ratioBarButton.setGeometry(QRect(10, 280, 171, 31))
        self.expandButton = QPushButton(self.mainWidget)
        self.expandButton.setObjectName(u"expandButton")
        self.expandButton.setGeometry(QRect(190, 10, 31, 300))

        self.setCentralWidget(self.mainWidget)
        self.menuBar = QMenuBar(self)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 520, 24))
        self.toolsMenu = QMenu(self.menuBar)
        self.toolsMenu.setObjectName(u"toolsMenu")
        self.setMenuBar(self.menuBar)
        QWidget.setTabOrder(self.selectorWidget, self.rankComboBox)
        QWidget.setTabOrder(self.rankComboBox, self.recipeListView)
        QWidget.setTabOrder(self.recipeListView, self.nameRadio)
        QWidget.setTabOrder(self.nameRadio, self.effectRadio)
        QWidget.setTabOrder(self.effectRadio, self.stuffRadio)
        QWidget.setTabOrder(self.stuffRadio, self.searchInput)
        QWidget.setTabOrder(self.searchInput, self.searchListView)
        QWidget.setTabOrder(self.searchListView, self.favoriteListView)
        QWidget.setTabOrder(self.favoriteListView, self.alignUpButton)
        QWidget.setTabOrder(self.alignUpButton, self.alignDownButton)
        QWidget.setTabOrder(self.alignDownButton, self.favoriteDeleteButton)
        QWidget.setTabOrder(self.favoriteDeleteButton, self.expandButton)
        QWidget.setTabOrder(self.expandButton, self.ratioBarButton)
        QWidget.setTabOrder(self.ratioBarButton, self.stuffRatio0)
        QWidget.setTabOrder(self.stuffRatio0, self.stuffRatio1)
        QWidget.setTabOrder(self.stuffRatio1, self.stuffRatio2)

        self.menuBar.addAction(self.toolsMenu.menuAction())
        self.toolsMenu.addAction(self.settingsAction)
        self.toolsMenu.addSeparator()
        self.toolsMenu.addAction(self.helpAction)

        self.retranslateUi()
        self.selectorWidget.setCurrentIndex(0)

        for item in recipeData['categories']:
            self.rankComboBox.addItem(item)

        # Actions
        self.ratioBarButton.clicked.connect(self.openCloseRatioDialog)
        self.expandButton.clicked.connect(self.toggleExpandedWindow)

        QMetaObject.connectSlotsByName(self)

    def createStatBox(self):
        pass

    def toggleExpandedWindow(self):
        if self._expanded:
            self.resize(231, 340)
            self.setFixedSize(QSize(231, 340))
        else:
            self.resize(520, 340)
            self.setFixedSize(QSize(520, 340))
        self._expanded = not self._expanded

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
        #     self._ratioDialog.update(data)

    # retranslateUi
    def retranslateUi(self):
        self.setWindowTitle("Spoon")
        self.settingsAction.setText("설정")
        self.helpAction.setText("도움말")
        self.ratiobox.setTitle("비율")

        # 비율 섹션
        # 재료 라벨
        self.stuffLabel0.setToolTip(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
        self.stuffLabel0.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">\uc7ac\ub8cc1</span></p></body></html>", None))
        self.stuffLabel1.setToolTip(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
        self.stuffLabel1.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">\uc7ac\ub8cc2</span></p></body></html>", None))
        self.stuffLabel2.setToolTip(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
        self.stuffLabel2.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">\uc7ac\ub8cc3</span></p></body></html>", None))

        # 재료 이름 라벨
        self.stuffName0.setToolTip(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
        self.stuffName0.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>recipe_C:C</p></body></html>", None))
        self.stuffName1.setToolTip(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
        self.stuffName1.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>recipe_D:D</p></body></html>", None))
        self.stuffName2.setToolTip(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
        self.stuffName2.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>recipe_E:E</p></body></html>", None))

        # % 기호 라벨
        self.percentLabel0.setToolTip(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
        self.percentLabel0.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" color:#aaaaaa;\">%</span></p></body></html>", None))
        self.percentLabel1.setToolTip(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
        self.percentLabel1.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" color:#aaaaaa;\">%</span></p></body></html>", None))
        self.percentLabel2.setToolTip(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><br/></p></body></html>", None))
        self.percentLabel2.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" color:#aaaaaa;\">%</span></p></body></html>", None))

        self.infoBox.setTitle(QCoreApplication.translate(
            "Spoon", u"\uc815\ubcf4", None))
        self.chrBox.setTitle("")
        self.statBox.setTitle("")
        self.defBox.setTitle("")
        self.atkBox.setTitle("")

        self.hpLabel.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" font-weight:600;\">HP</span></p></body></html>", None))
        self.mpLabel.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" font-weight:600;\">MP</span></p></body></html>", None))
        self.hpValue.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>r_K</p></body></html>", None))
        self.spLabel.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" font-weight:600;\">SP</span></p></body></html>", None))
        self.mpValue.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>r_L</p></body></html>", None))
        self.spValue.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>r_M</p></body></html>", None))

        self.strValue.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>r_F</p></body></html>", None))
        self.strLabel.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" font-weight:600;\">\uccb4\ub825</span></p></body></html>", None))
        self.intValue.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>r_G</p></body></html>", None))
        self.lucValue.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>r_J</p></body></html>", None))
        self.lucLabel.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" font-weight:600;\">\ud589\uc6b4</span></p></body></html>", None))
        self.intLabel.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" font-weight:600;\">\uc9c0\ub825</span></p></body></html>", None))
        self.wilLabel.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" font-weight:600;\">\uc758\uc9c0</span></p></body></html>", None))
        self.wilValue.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>r_I</p></body></html>", None))
        self.dexLabel.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" font-weight:600;\">\uc19c\uc528</span></p></body></html>", None))
        self.dexValue.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>r_H</p></body></html>", None))

        self.mdfLabel.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" font-weight:600;\">\ub9c8\ubc29</span></p></body></html>", None))
        self.defLabel.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" font-weight:600;\">\ubc29\uc5b4</span></p></body></html>", None))
        self.mptLabel.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" font-weight:600;\">\ub9c8\ubcf4</span></p></body></html>", None))
        self.defValue.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>r_Q</p></body></html>", None))
        self.prtLabel.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" font-weight:600;\">\ubcf4\ud638</span></p></body></html>", None))
        self.mptValue.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>r_T</p></body></html>", None))
        self.prtValue.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>r_R</p></body></html>", None))
        self.mdfValue.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>r_S</p></body></html>", None))

        self.eftValue.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>r_U</p></body></html>", None))
        self.mtkValue.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>r_P</p></body></html>", None))
        self.eftLabel.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" font-weight:600;\">\ud6a8\uacfc</span></p></body></html>", None))
        self.minDamValue.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>r_N</p></body></html>", None))
        self.maxDamValue.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" font-weight:600;\">\ub9e5\ub310</span></p></body></html>", None))
        self.maxDamLabel.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" font-weight:600;\">\ubbfc\ub310</span></p></body></html>", None))
        self.minDamLabel.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p>r_O</p></body></html>", None))
        self.mtkLabel.setText(QCoreApplication.translate(
            "Spoon", u"<html><head/><body><p><span style=\" font-weight:600;\">\ub9c8\uacf5</span></p></body></html>", None))
        self.selectorWidget.setTabText(self.selectorWidget.indexOf(
            self.recipeListMenu), QCoreApplication.translate("Spoon", u"\ubaa9\ub85d", None))
        self.nameRadio.setText(QCoreApplication.translate(
            "Spoon", u"\uc774\ub984", None))
        self.effectRadio.setText(QCoreApplication.translate(
            "Spoon", u"\ud6a8\uacfc", None))
        self.stuffRadio.setText(QCoreApplication.translate(
            "Spoon", u"\uc7ac\ub8cc", None))
        self.selectorWidget.setTabText(self.selectorWidget.indexOf(
            self.searchMenu), QCoreApplication.translate("Spoon", u"\uac80\uc0c9", None))

        self.alignUpButton.setText(
            QCoreApplication.translate("Spoon", u"\u25b3", None))
        self.alignDownButton.setText(
            QCoreApplication.translate("Spoon", u"\u25bd", None))
        self.favoriteDeleteButton.setText(
            QCoreApplication.translate("Spoon", u"\uc0ad\uc81c", None))

        self.selectorWidget.setTabText(self.selectorWidget.indexOf(
            self.favoriteMenu), QCoreApplication.translate("Spoon", u"\u2606", None))
        self.ratioBarButton.setText(QCoreApplication.translate(
            "Spoon", u"\ube44\uc728 \ubc14 On / Off", None))
        self.expandButton.setText(
            QCoreApplication.translate("Spoon", u"\u300b", None))
        self.toolsMenu.setTitle(QCoreApplication.translate(
            "Spoon", u"\ub3c4\uad6c", None))
