# -*- coding: utf-8 -*-
'''
# Main window for Spoon
# Made by kry-p
# https://github.com/kry-p/Teaspoon-mabinogi
'''

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize,
                            Qt)
from PySide6.QtGui import (QAction, QFont, QStandardItem,
                           QStandardItemModel)
from PySide6.QtWidgets import (QComboBox, QGroupBox, QLabel, QLineEdit,
                               QListView, QMainWindow, QMenu, QMenuBar,
                               QPushButton, QRadioButton, QSizePolicy,
                               QTabWidget, QWidget)
from . import (database_manager)
from .settings_dialog import SettingsDialog
from .ratio_dialog import RatioDialog
from .preferences_provider import (preferences, watcher, init, getPreferences)

db = database_manager.DBManager()
CATEGORIES = db.getCategories()
COLOR_POSITIVE = '#0099FF'
COLOR_NEGATIVE = '#FF0000'
STYLE_BOLD = 'font-weight: 600;'

# 메인 윈도우
class FullWindow(QMainWindow):
    def __init__(self, version):
        super().__init__()
        init()

        self.version = version
        self.ratioDialog = None
        self.settingsDialog = None
        self.expanded = getPreferences('initialWindowExpanded')
        self.currentFood = getPreferences('currentFood')
        self.favorites = [] if getPreferences('favorites')['item'] is None else getPreferences('favorites')['item']

        self.setWindow()  # 윈도우 기본 설정
        self.createMenuBar()  # 메뉴 바
        self.createStuffBox()  # 비율 박스
        self.createInfoBox()  # 요리 정보 박스
        self.createLeftToolBox()  # 왼쪽 툴박스

        # 기타 버튼
        self.ratioBarButton = QPushButton(self.mainWidget)
        self.ratioBarButton.setGeometry(QRect(9, 280, 201, 31))

        self.setCentralWidget(self.mainWidget)
        self.selectorWidget.setCurrentIndex(0)

        # 액션
        self.ratioBarButton.clicked.connect(self.openCloseRatioDialog)
        self.recipeListView.doubleClicked.connect(self.listAddToFavorites)
        self.searchListView.doubleClicked.connect(self.searchAddToFavorites)
        self.actions['settings'].triggered.connect(self.openSettingsDialog)
        self.actions['lockRatio'].triggered.connect(self.toggleLockRatioBar)
        self.rankComboBox.currentIndexChanged.connect(self.changeCategory)
        self.recipeListSelectionModel.currentChanged.connect(
            self.onRecipeListViewValueChanged)
        self.searchListSelectionModel.currentChanged.connect(
            self.onSearchListViewValueChanged)
        self.favoriteListSelectionModel.currentChanged.connect(
            self.onFavoriteListViewValueChanged)
        self.alignUpButton.clicked.connect(self.onChangeFavoriteOrderUp)
        self.alignDownButton.clicked.connect(self.onChangeFavoriteOrderDown)
        self.favoriteDeleteButton.clicked.connect(self.deleteSelectedFavorite)
        self.searchButton.clicked.connect(self.search)

        # Settings watcher
        watcher.fileChanged.connect(self.onFileChanged)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    # 설정 파일 내용 바뀔 시
    def onFileChanged(self):
        # 즐겨찾기 초기화 감지
        favorites = getPreferences('favorites')['item']
        if favorites is not None:
            if len(favorites) == 0:
                self.favorites = []
                self.updateFavoriteList()

    """ ********** UI ********** """
    # 창 기본 설정
    def setWindow(self):
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(520, 340))
        self.setMaximumSize(QSize(520, 340))
        self.setFixedSize(QSize(520, 340))
        self.mainWidget = QWidget(self)

    # 메뉴 바
    def createMenuBar(self):
        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 520, 24))
        self.toolsMenu = QMenu(self.menuBar)
        self.setMenuBar(self.menuBar)
        self.actions = {
            'lockRatio': QAction(self),
            'changeMode': QAction(self),
            'settings': QAction(self),
            'help': QAction(self)
        }
        self.actions['lockRatio'].setCheckable(True)
        self.actions['lockRatio'].setChecked(
            True if getPreferences('ratioBarLocked') == 'true' else False)
        self.actions['changeMode'].setEnabled(False)
        self.actions['help'].setEnabled(False)

        self.menuBar.addAction(self.toolsMenu.menuAction())
        self.toolsMenu.addAction(self.actions['lockRatio'])
        self.toolsMenu.addAction(self.actions['changeMode'])
        self.toolsMenu.addSeparator()
        self.toolsMenu.addAction(self.actions['settings'])
        self.toolsMenu.addAction(self.actions['help'])

    # 좌측 툴박스
    def createLeftToolBox(self):
        self.selectorWidget = QTabWidget(self.mainWidget)
        self.selectorWidget.setGeometry(QRect(10, 10, 201, 271))

        self.recipeListMenu = QWidget()
        self.searchMenu = QWidget()
        self.favoriteMenu = QWidget()

        self.createLeftFirstTab()
        self.createLeftSecondTab()
        self.createLeftThirdTab()

    def createLeftFirstTab(self):
        self.rankComboBox = QComboBox(self.recipeListMenu)
        self.rankComboBox.setGeometry(QRect(12, 10, 171, 22))
        self.recipeListView = QListView(self.recipeListMenu)
        self.recipeListView.setGeometry(QRect(12, 40, 171, 187))
        self.recipeListModel = QStandardItemModel()
        self.recipeListView.setModel(self.recipeListModel)
        self.recipeListSelectionModel = self.recipeListView.selectionModel()

        self.rankComboBox.addItems(CATEGORIES['categoryName'])
        self.rankComboBox.setCurrentIndex(
            int(getPreferences('currentCategoryIndex')))

        self.getCurrentCategoryList()
        if self.currentFood != '':
            self.setFoodInfo(self.currentFood)

    def createLeftSecondTab(self):
        self.searchInput = QLineEdit(self.searchMenu)
        self.searchInput.setGeometry(QRect(12, 30, 126, 21))
        self.searchListView = QListView(self.searchMenu)
        self.searchListView.setGeometry(QRect(12, 56, 171, 171))
        self.searchButton = QPushButton(self.searchMenu)
        self.searchButton.setGeometry(138, 29, 46, 23)
        self.searchListModel = QStandardItemModel()
        self.searchListView.setModel(self.searchListModel)
        self.searchListSelectionModel = self.searchListView.selectionModel()
        self.nameRadio = QRadioButton(self.searchMenu)
        self.nameRadio.setGeometry(QRect(15, 10, 45, 16))
        self.effectRadio = QRadioButton(self.searchMenu)
        self.effectRadio.setGeometry(QRect(76, 10, 45, 16))
        self.stuffRadio = QRadioButton(self.searchMenu)
        self.stuffRadio.setGeometry(QRect(138, 10, 45, 16))

        self.setTabOrder(self.searchInput, self.searchButton)
        self.setTabOrder(self.searchButton, self.searchListView)

        self.nameRadio.setChecked(True)

    def createLeftThirdTab(self):
        self.favoriteListView = QListView(self.favoriteMenu)
        self.favoriteListView.setGeometry(QRect(12, 10, 171, 195))
        self.favoriteListModel = QStandardItemModel()
        self.favoriteListView.setModel(self.favoriteListModel)
        self.favoriteListSelectionModel = self.favoriteListView.selectionModel()
        self.favoriteListViewModel = self.favoriteListView.model()

        self.updateFavoriteList()

        self.alignUpButton = QPushButton(self.favoriteMenu)
        self.alignUpButton.setGeometry(QRect(11, 210, 31, 23))
        self.alignDownButton = QPushButton(self.favoriteMenu)
        self.alignDownButton.setGeometry(QRect(39, 210, 31, 23))
        self.favoriteDeleteButton = QPushButton(self.favoriteMenu)
        self.favoriteDeleteButton.setGeometry(QRect(132, 210, 51, 23))

        self.selectorWidget.addTab(self.recipeListMenu, '')
        self.selectorWidget.addTab(self.searchMenu, '')
        self.selectorWidget.addTab(self.favoriteMenu, '')

    # 비율 박스
    def createStuffBox(self):
        # 비율 입력 박스
        self.ratioBox = QGroupBox(self.mainWidget)
        self.ratioBox.setGeometry(QRect(215, 10, 295, 121))

        self.stuffLabels = [
            QLabel(self.ratioBox), QLabel(self.ratioBox), QLabel(self.ratioBox)
        ]
        self.stuffNames = [
            QLabel(self.ratioBox), QLabel(self.ratioBox), QLabel(self.ratioBox)
        ]
        self.percentLabels = [
            QLabel(self.ratioBox), QLabel(self.ratioBox), QLabel(self.ratioBox)
        ]
        self.stuffRatioInputs = [
            QLineEdit(self.ratioBox), QLineEdit(
                self.ratioBox), QLineEdit(self.ratioBox)
        ]

        for i in range(0, 3):
            self.stuffLabels[i].setGeometry(QRect(10, 30 + i * 30, 41, 20))
            self.stuffNames[i].setGeometry(QRect(60, 30 + i * 30, 121, 20))
            self.percentLabels[i].setGeometry(QRect(260, 30 + i * 30, 21, 20))
            self.stuffRatioInputs[i].setGeometry(
                QRect(215, 30 + i * 30, 41, 20))
            self.stuffRatioInputs[i].setEnabled(False) 

    # 정보 박스
    def createInfoBox(self):
        self.infoBox = QGroupBox(self.mainWidget)
        self.infoBox.setGeometry(QRect(215, 130, 295, 181))

        self.createChrBox()
        self.createStatBox()
        self.createAtkBox()
        self.createDefBox()

    # HP, MP, SP 박스
    def createChrBox(self):
        self.chrBox = QGroupBox(self.infoBox)
        self.chrBox.setGeometry(QRect(10, 20, 275, 31))

        self.hpLabel = QLabel(self.chrBox)
        self.hpLabel.setGeometry(QRect(10, 10, 31, 16))
        self.hpValue = QLabel(self.chrBox)
        self.hpValue.setGeometry(QRect(40, 10, 31, 16))

        self.mpLabel = QLabel(self.chrBox)
        self.mpLabel.setGeometry(QRect(105, 10, 31, 16))
        self.mpValue = QLabel(self.chrBox)
        self.mpValue.setGeometry(QRect(135, 10, 31, 16))

        self.spLabel = QLabel(self.chrBox)
        self.spLabel.setGeometry(QRect(200, 10, 31, 16))
        self.spValue = QLabel(self.chrBox)
        self.spValue.setGeometry(QRect(230, 10, 31, 16))

    # 기초 스테이터스 박스
    def createStatBox(self):
        self.statBox = QGroupBox(self.infoBox)
        self.statBox.setGeometry(QRect(10, 60, 86, 111))

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

    # 방어 스테이터스 박스
    def createDefBox(self):
        self.defBox = QGroupBox(self.infoBox)
        self.defBox.setGeometry(QRect(105, 60, 85, 111))

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

    # 공격 스테이터스 박스
    def createAtkBox(self):
        self.atkBox = QGroupBox(self.infoBox)
        self.atkBox.setStyleSheet(
            'padding: 0px 0px 0px 0px; margin: 0px 0px 0px 0px;')
        self.atkBox.setGeometry(QRect(199, 60, 86, 111))

        self.eftLabel = QLabel(self.atkBox)
        self.eftLabel.setGeometry(QRect(10, 90, 31, 16))
        self.eftValue = QLabel(self.atkBox)
        self.eftValue.setGeometry(QRect(40, 90, 31, 16))
        self.eftValue.setFont(QFont('NanumGothic', 7))
        self.mtkLabel = QLabel(self.atkBox)
        self.mtkLabel.setGeometry(QRect(10, 63, 31, 16))
        self.mtkValue = QLabel(self.atkBox)
        self.mtkValue.setGeometry(QRect(40, 63, 31, 16))

        self.minDamLabel = QLabel(self.atkBox)
        self.minDamLabel.setGeometry(QRect(10, 10, 31, 16))
        self.minDamValue = QLabel(self.atkBox)
        self.minDamValue.setGeometry(QRect(40, 10, 31, 16))
        self.maxDamLabel = QLabel(self.atkBox)
        self.maxDamLabel.setGeometry(QRect(10, 37, 31, 16))
        self.maxDamValue = QLabel(self.atkBox)
        self.maxDamValue.setGeometry(QRect(40, 37, 31, 16))

    """ ********** 액션 ********** """
    # 비율 바 잠금
    def toggleLockRatioBar(self):
        preferences.setValue('ratioBarLocked',
                            self.actions['lockRatio'].isChecked())

    # 현재 카테고리의 리스트 가져오기
    def getCurrentCategoryList(self):
        self.recipeListModel.clear()
        currentCategoryItems = db.getFoods(
            CATEGORIES['categoryCode'][self.rankComboBox.currentIndex()])

        for item in currentCategoryItems:
            currentItem = QStandardItem(item[0])
            currentItem.setEditable(False)
            self.recipeListModel.appendRow(currentItem)

    # 목록 뷰에서 값이 바뀔 때
    def onRecipeListViewValueChanged(self):
        currentIndex = self.recipeListSelectionModel.currentIndex().row()

        if currentIndex != -1:
            currentFood = self.recipeListModel.item(currentIndex, 0).text()
            preferences.setValue('currentFood', currentFood)
            self.setFoodInfo(currentFood)

    # 요리 정보를 표시
    def setFoodInfo(self, foodName):
        statValues = [self.strValue, self.intValue, self.dexValue, self.wilValue, self.lucValue,
                 self.hpValue, self.mpValue, self.spValue,
                 self.minDamValue, self.maxDamValue, self.mtkValue,
                 self.defValue, self.prtValue, self.mdfValue, self.mptValue]
        info = db.getFoodInfo(foodName)
        ingredients = info['ingredients'][0]
        ratio = info['ratio'][0]
        special = info['specialEffects'][0]
        stats = info['stats'][0]

        for i in range(0, 3):
            if ingredients[i] is None:
                self.stuffNames[i].setText('')
                self.stuffRatioInputs[i].setText('')
            else:
                self.stuffNames[i].setText(ingredients[i])
                self.stuffRatioInputs[i].setText(str(int(ratio[i])))

        self.eftValue.setText('' if special[0] is None else special[0])
        for idx in range(len(statValues)):
            val = stats[idx]

            if val is not None:
                statValues[idx].setText('' if stats[idx] is None else str(int(stats[idx])))
                if int(val) > 0:
                    statValues[idx].setStyleSheet('color: %s;' % COLOR_POSITIVE)
                else:
                    statValues[idx].setStyleSheet('color: %s;' % COLOR_NEGATIVE)

    # 설정 창 열기
    def openSettingsDialog(self, food):
        if self.settingsDialog is None:
            self.settingsDialog = SettingsDialog()
        self.settingsDialog.show()

    # 즐겨찾기에 추가 (목록)
    def listAddToFavorites(self):
        currentIndex = self.recipeListSelectionModel.currentIndex().row()
        if currentIndex != -1:
            selected = self.recipeListModel.item(currentIndex, 0).text()
            self.favorites.append(selected)
            self.favorites = list(dict.fromkeys(self.favorites))
            preferences.setValue('favorites', {'item': self.favorites})
            self.updateFavoriteList()

    # 즐겨찾기에 추가 (검색)
    def searchAddToFavorites(self):
        currentIndex = self.searchListSelectionModel.currentIndex().row()
        if currentIndex != -1:
            selected = self.searchListModel.item(currentIndex, 0).text()
            self.favorites.append(selected)
            self.favorites = list(dict.fromkeys(self.favorites))
            preferences.setValue('favorites', {
                'item': self.favorites
            })
            self.updateFavoriteList()

    # 즐겨챶기 뷰에서 선택된 요리가 바뀔 때
    def onFavoriteListViewValueChanged(self):
        currentIndex = self.favoriteListSelectionModel.currentIndex().row()
        if currentIndex != -1:
            preferences.setValue(
                'currentFood', self.favoriteListModel.item(currentIndex, 0).text())
            self.setFoodInfo(self.favoriteListModel.item(currentIndex, 0).text())

    # 검색 뷰에서 선택된 요리가 바뀔 때
    def onSearchListViewValueChanged(self):
        currentIndex = self.searchListSelectionModel.currentIndex().row()
        if currentIndex != -1:
            currentFood = self.searchListModel.item(currentIndex, 0).text()
            preferences.setValue(
                'currentFood', currentFood)
            self.setFoodInfo(currentFood)

    # 즐겨찾기 목록 가져오기
    def updateFavoriteList(self):
        self.favoriteListModel.clear()

        if self.favorites is not None:
            for item in self.favorites:
                currentItem = QStandardItem(item)
                currentItem.setEditable(False)
                self.favoriteListModel.appendRow(currentItem)

    # 선택된 즐겨찾기 요리를 위로
    def onChangeFavoriteOrderUp(self):
        currentPos = self.favoriteListSelectionModel.currentIndex().row()
        if currentPos > 0:
            temp = self.favorites[currentPos - 1]
            self.favorites[currentPos - 1] = self.favorites[currentPos]
            self.favorites[currentPos] = temp
            self.updateFavoriteList()
            self.favoriteListView.setCurrentIndex(self.favoriteListViewModel.index(currentPos - 1, 0))

    # 선택된 즐겨찾기 요리를 아래로
    def onChangeFavoriteOrderDown(self):
        currentPos = self.favoriteListSelectionModel.currentIndex().row()

        if currentPos != -1 and currentPos < (len(self.favorites) - 1):
            temp = self.favorites[currentPos + 1]
            self.favorites[currentPos + 1] = self.favorites[currentPos]
            self.favorites[currentPos] = temp
            self.updateFavoriteList()
            self.favoriteListView.setCurrentIndex(self.favoriteListViewModel.index(currentPos + 1, 0))

    # 선택된 즐겨찾기 요리 삭제
    def deleteSelectedFavorite(self):
        currentPos = self.favoriteListSelectionModel.currentIndex().row()
        if currentPos != -1:
            self.favorites.pop(currentPos)
            self.updateFavoriteList()
            preferences.setValue('favorites', {
                'item':self.favorites
            })

    # 검색
    def search(self):
        currentText = self.searchInput.text()
        currentEnabled = -1

        if self.nameRadio.isChecked():
            currentEnabled = 0
        elif self.effectRadio.isChecked():
            currentEnabled = 1
        elif self.stuffRadio.isChecked():
            currentEnabled = 2

        if currentText != '' and currentEnabled != -1:
            self.searchListModel.clear()
            result = list()
            
            if currentEnabled == 0:
                try:
                    result = db.searchByName(currentText)
                except:
                    result = None
            if currentEnabled == 1:
                categories = ["체력", "지력", "솜씨", "의지", "행운",
                              "HP", "MP", "SP",
                              "민댐", "맥댐", "마공",
                              "방어", "보호", "마방", "마보", "효과"]
                query = list()
                for idx in range(len(categories)):
                    if categories[idx] in currentText:
                        query.append(True)
                    else:
                        query.append(False)
                try:
                    result = db.searchByEffect(query)
                except:
                    result = None
            if currentEnabled == 2:
                try:
                    result = db.searchByIngredient(currentText)
                except:
                    result = None
                
            if result is not None:
                for item in result:
                    currentItem = QStandardItem(item[0])
                    currentItem.setEditable(False)
                    self.searchListModel.appendRow(currentItem)
                
    # 현재 카테고리 변경
    def changeCategory(self):
        preferences.setValue('currentCategoryIndex',
                          self.rankComboBox.currentIndex())
        self.getCurrentCategoryList()

    # 비율 바 열기 / 닫기
    def openCloseRatioDialog(self):
        data = list(map(lambda value: 0 if value.text() ==
                        '' else int(value.text()), self.stuffRatioInputs))
        test = sum(data)
        if self.ratioDialog is None and test != 0:
            self.ratioDialog = RatioDialog(data)
        else:
            if self.ratioDialog is not None:
                self.ratioDialog.close()
            self.ratioDialog = None

    # 종료 시
    def closeEvent(self, event):
        if self.ratioDialog:
            self.ratioDialog.close()
        if self.settingsDialog:
            self.settingsDialog.close()
    
    # 키 이벤트
    def keyPressEvent(self, event):
        # Enter 버튼을 누를 때 검색
        if self.selectorWidget.currentIndex() == 1:
            if event.key() == Qt.Key_Return:
                self.searchButton.click()

    # 텍스트 지정
    def retranslateUi(self):
        # 제목
        self.setWindowTitle('Spoon %s' % self.version)

        # 메뉴 바
        self.actions['lockRatio'].setText('비율 바 잠금')
        self.actions['changeMode'].setText('모드 변경 (공사 중)')
        self.actions['settings'].setText('설정')
        self.actions['help'].setText('도움말 (공사 중)')

        # 비율 섹션
        self.ratioBox.setTitle('비율')
        
        # 검색
        self.nameRadio.setText('이름')
        self.effectRadio.setText('효과')
        self.stuffRadio.setText('재료')
        self.searchButton.setText('검색')

        # 재료 라벨
        for i in range(0, 3):
            self.stuffLabels[i].setText('재료%d' % (i + 1))
            self.stuffLabels[i].setStyleSheet(STYLE_BOLD)
            self.percentLabels[i].setText('%')  # % 기호 라벨

        self.infoBox.setTitle('정보')

        self.hpLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>HP</span></p></body></html>', None))
        self.mpLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>MP</span></p></body></html>', None))
        self.spLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>SP</span></p></body></html>', None))

        self.strLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\uccb4\ub825</span></p></body></html>', None))
        self.lucLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ud589\uc6b4</span></p></body></html>', None))
        self.intLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\uc9c0\ub825</span></p></body></html>', None))
        self.wilLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\uc758\uc9c0</span></p></body></html>', None))
        self.dexLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\uc19c\uc528</span></p></body></html>', None))

        self.mdfLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ub9c8\ubc29</span></p></body></html>', None))
        self.defLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ubc29\uc5b4</span></p></body></html>', None))
        self.mptLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ub9c8\ubcf4</span></p></body></html>', None))
        self.prtLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ubcf4\ud638</span></p></body></html>', None))

        self.minDamLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ubbfc\ub310</span></p></body></html>', None))
        self.maxDamLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ub9e5\ub310</span></p></body></html>', None))
        self.mtkLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ub9c8\uacf5</span></p></body></html>', None))
        self.eftLabel.setText(QCoreApplication.translate(
            'Spoon', u'<html><head/><body><p><span style=\' font-weight:600;\'>\ud6a8\uacfc</span></p></body></html>', None))

        self.selectorWidget.setTabText(self.selectorWidget.indexOf(
            self.recipeListMenu), QCoreApplication.translate('Spoon', u'\ubaa9\ub85d', None))
        self.selectorWidget.setTabText(self.selectorWidget.indexOf(
            self.searchMenu), QCoreApplication.translate('Spoon', u'\uac80\uc0c9', None))
        self.selectorWidget.setTabText(self.selectorWidget.indexOf(
            self.favoriteMenu), QCoreApplication.translate('Spoon', u'\u2606', None))

        self.alignUpButton.setText(
            QCoreApplication.translate('Spoon', u'\u25b3', None))
        self.alignDownButton.setText(
            QCoreApplication.translate('Spoon', u'\u25bd', None))
        self.favoriteDeleteButton.setText(
            QCoreApplication.translate('Spoon', u'\uc0ad\uc81c', None))

        self.ratioBarButton.setText(QCoreApplication.translate(
            'Spoon', u'\ube44\uc728 \ubc14 On / Off', None))
        self.toolsMenu.setTitle(QCoreApplication.translate(
            'Spoon', u'\ub3c4\uad6c', None))
