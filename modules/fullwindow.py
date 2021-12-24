# -*- coding: utf-8 -*-
'''
# Main window for Spoon
# Made by kry-p
# https://github.com/kry-p/Teaspoon-mabinogi
'''

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize,
                            Qt)
from PySide6.QtGui import (QAction, QStandardItem, QStandardItemModel)
from PySide6.QtWidgets import (QComboBox, QGroupBox, QLabel, QLineEdit,
                               QListView, QMainWindow, QMenu, QMenuBar,
                               QPushButton, QRadioButton, QSizePolicy,
                               QTabWidget, QWidget)

from modules.elements import Widget
from . import database_manager
from .settings_dialog import SettingsDialog
from .ratio_dialog import RatioDialog
from .preferences_provider import (preferences, watcher, init, getPreferences)

db = database_manager.DBManager()
CATEGORIES = db.getCategories()
COLOR_POSITIVE = '#0099FF'
COLOR_NEGATIVE = '#FF0000'
STYLE_BOLD = 'font-weight: 600;'

# Main window (Full)
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

        self.setWindow()  # Settings for window
        self.createMenuBar()  # Menu bar
        self.createStuffBox()  # Stuff ratio box
        self.createInfoBox()  # Information box
        self.createLeftToolBox()  # Left toolbox

        # Misc. buttons
        self.ratioBarButton = QPushButton(self.mainWidget)
        self.ratioBarButton.setGeometry(QRect(9, 280, 201, 31))

        self.setCentralWidget(self.mainWidget)
        self.selectorWidget.setCurrentIndex(0)

        # Actions
        self.ratioBarButton.clicked.connect(self.toggleOpenRatioDialog)
        self.recipeListView.doubleClicked.connect(self.listAddToFavorites)
        self.searchListView.doubleClicked.connect(self.searchAddToFavorites)
        self.actions['settings'].triggered.connect(self.openSettingsDialog)
        self.actions['lockRatio'].triggered.connect(self.toggleLockRatioBar)
        self.rankComboBox.currentIndexChanged.connect(self.onChangeCategory)
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

    # If QSettings file has changed
    def onFileChanged(self):
        # Detects 
        favorites = getPreferences('favorites')['item']
        if favorites is not None:
            if len(favorites) == 0:
                self.favorites = []
                self.updateFavoriteList()

    """ ********** UI ********** """
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

    def createStuffBox(self):
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

    def createInfoBox(self):
        self.infoBox = QGroupBox(self.mainWidget)
        self.infoBox.setGeometry(QRect(215, 130, 295, 181))

        self.createChrBox()
        self.createStatBox()
        self.createAtkBox()
        self.createDefBox()

    def createChrBox(self):
        self.chrBox = QGroupBox(self.infoBox)
        self.chrBox.setGeometry(QRect(10, 20, 275, 31))

        self.chrLabel = [        
            Widget(widget = QLabel(self.chrBox), geometry = QRect(10, 10, 31, 16), text = 'HP', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.chrBox), geometry = QRect(105, 10, 31, 16), text = 'MP', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.chrBox), geometry = QRect(200, 10, 31, 16), text = 'SP', stylesheet = STYLE_BOLD)
        ]
        self.chrValue = [
            Widget(widget = QLabel(self.chrBox), geometry = QRect(40, 10, 31, 16)),
            Widget(widget = QLabel(self.chrBox), geometry = QRect(135, 10, 31, 16)),
            Widget(widget = QLabel(self.chrBox), geometry = QRect(230, 10, 31, 16))        
        ]

    def createStatBox(self):
        self.statBox = QGroupBox(self.infoBox)
        self.statBox.setGeometry(QRect(10, 60, 86, 111))

        self.statLabel = [
            Widget(widget = QLabel(self.statBox), geometry = QRect(10, 10, 31, 16), text = '체력', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.statBox), geometry = QRect(10, 30, 31, 16), text = '지력', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.statBox), geometry = QRect(10, 50, 31, 16), text = '솜씨', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.statBox), geometry = QRect(10, 70, 31, 16), text = '의지', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.statBox), geometry = QRect(10, 90, 31, 16), text = '행운', stylesheet = STYLE_BOLD)
        ]
        self.statValue = [
            Widget(widget = QLabel(self.statBox), geometry = QRect(40, 10, 31, 16)),
            Widget(widget = QLabel(self.statBox), geometry = QRect(40, 30, 31, 16)),
            Widget(widget = QLabel(self.statBox), geometry = QRect(40, 50, 31, 16)),
            Widget(widget = QLabel(self.statBox), geometry = QRect(40, 70, 31, 16)),
            Widget(widget = QLabel(self.statBox), geometry = QRect(40, 90, 31, 16)),
        ]

    def createDefBox(self):
        self.defBox = QGroupBox(self.infoBox)
        self.defBox.setGeometry(QRect(105, 60, 85, 111))

        self.defLabel = [
            Widget(widget = QLabel(self.defBox), geometry = QRect(10, 10, 31, 16), text = '방어', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.defBox), geometry = QRect(10, 37, 31, 16), text = '보호', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.defBox), geometry = QRect(10, 63, 31, 16), text = '마방', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.defBox), geometry = QRect(10, 90, 31, 16), text = '마보', stylesheet = STYLE_BOLD),
        ]

        self.defValue = [
            Widget(widget = QLabel(self.defBox), geometry = QRect(40, 10, 31, 16)),
            Widget(widget = QLabel(self.defBox), geometry = QRect(40, 37, 31, 16)),
            Widget(widget = QLabel(self.defBox), geometry = QRect(40, 63, 31, 16)),
            Widget(widget = QLabel(self.defBox), geometry = QRect(40, 90, 31, 16)),
        ]
    
    def createAtkBox(self):
        self.atkBox = QGroupBox(self.infoBox)
        self.atkBox.setGeometry(QRect(199, 60, 86, 111))

        self.atkLabel = [
            Widget(widget = QLabel(self.atkBox), geometry = QRect(10, 10, 31, 16), text = '민댐', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.atkBox), geometry = QRect(10, 37, 31, 16), text = '맥댐', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.atkBox), geometry = QRect(10, 63, 31, 16), text = '마공', stylesheet = STYLE_BOLD),
        ]

        self.atkValue = [
            Widget(widget = QLabel(self.atkBox), geometry = QRect(40, 10, 31, 16)),
            Widget(widget = QLabel(self.atkBox), geometry = QRect(40, 37, 31, 16)),
            Widget(widget = QLabel(self.atkBox), geometry = QRect(40, 63, 31, 16)),
        ]

        self.eftLabel = QLabel(self.atkBox)
        self.eftLabel.setGeometry(QRect(10, 90, 31, 16))
        self.eftValue = QLabel(self.atkBox)
        self.eftValue.setGeometry(QRect(40, 90, 31, 16))

    """ ********** 액션 ********** """
    def toggleLockRatioBar(self):
        preferences.setValue('ratioBarLocked',
                            self.actions['lockRatio'].isChecked())

    def getCurrentCategoryList(self):
        self.recipeListModel.clear()
        currentCategoryItems = db.getFoods(
            CATEGORIES['categoryCode'][self.rankComboBox.currentIndex()])

        for item in currentCategoryItems:
            currentItem = QStandardItem(item[0])
            currentItem.setEditable(False)
            self.recipeListModel.appendRow(currentItem)

    def onRecipeListViewValueChanged(self):
        currentIndex = self.recipeListSelectionModel.currentIndex().row()

        if currentIndex != -1:
            currentFood = self.recipeListModel.item(currentIndex, 0).text()
            preferences.setValue('currentFood', currentFood)
            self.setFoodInfo(currentFood)

    def setFoodInfo(self, foodName):
        statValues = self.statValue + self.chrValue\
                + self.atkValue + self.defValue
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
        self.eftValue.setToolTip('효과 없음' if special[1] is None else special[1])

        for idx in range(len(statValues)):
            val = stats[idx]

            statValues[idx].setText('' if stats[idx] is None else str(int(stats[idx])))
            
            if val is not None and int(val) > 0:
                statValues[idx].setStyleSheet('color: %s;' % COLOR_POSITIVE)
            else:
                statValues[idx].setStyleSheet('color: %s;' % COLOR_NEGATIVE)

    def openSettingsDialog(self, food):
        if self.settingsDialog is None:
            self.settingsDialog = SettingsDialog()
        self.settingsDialog.show()

    def listAddToFavorites(self):
        currentIndex = self.recipeListSelectionModel.currentIndex().row()
        if currentIndex != -1:
            selected = self.recipeListModel.item(currentIndex, 0).text()
            self.favorites.append(selected)
            self.favorites = list(dict.fromkeys(self.favorites))
            preferences.setValue('favorites', {'item': self.favorites})
            self.updateFavoriteList()

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

    def onFavoriteListViewValueChanged(self):
        currentIndex = self.favoriteListSelectionModel.currentIndex().row()
        if currentIndex != -1:
            preferences.setValue(
                'currentFood', self.favoriteListModel.item(currentIndex, 0).text())
            self.setFoodInfo(self.favoriteListModel.item(currentIndex, 0).text())

    def onSearchListViewValueChanged(self):
        currentIndex = self.searchListSelectionModel.currentIndex().row()
        if currentIndex != -1:
            currentFood = self.searchListModel.item(currentIndex, 0).text()
            preferences.setValue(
                'currentFood', currentFood)
            self.setFoodInfo(currentFood)

    def updateFavoriteList(self):
        self.favoriteListModel.clear()

        if self.favorites is not None:
            for item in self.favorites:
                currentItem = QStandardItem(item)
                currentItem.setEditable(False)
                self.favoriteListModel.appendRow(currentItem)

    def onChangeFavoriteOrderUp(self):
        currentPos = self.favoriteListSelectionModel.currentIndex().row()
        if currentPos > 0:
            temp = self.favorites[currentPos - 1]
            self.favorites[currentPos - 1] = self.favorites[currentPos]
            self.favorites[currentPos] = temp
            self.updateFavoriteList()
            self.favoriteListView.setCurrentIndex(self.favoriteListViewModel.index(currentPos - 1, 0))

    def onChangeFavoriteOrderDown(self):
        currentPos = self.favoriteListSelectionModel.currentIndex().row()

        if currentPos != -1 and currentPos < (len(self.favorites) - 1):
            temp = self.favorites[currentPos + 1]
            self.favorites[currentPos + 1] = self.favorites[currentPos]
            self.favorites[currentPos] = temp
            self.updateFavoriteList()
            self.favoriteListView.setCurrentIndex(self.favoriteListViewModel.index(currentPos + 1, 0))

    def deleteSelectedFavorite(self):
        currentPos = self.favoriteListSelectionModel.currentIndex().row()
        if currentPos != -1:
            self.favorites.pop(currentPos)
            self.updateFavoriteList()
            preferences.setValue('favorites', {
                'item':self.favorites
            })

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
                
    def onChangeCategory(self):
        preferences.setValue('currentCategoryIndex',
                          self.rankComboBox.currentIndex())
        self.getCurrentCategoryList()

    def toggleOpenRatioDialog(self):
        data = list(map(lambda value: 0 if value.text() ==
                        '' else int(value.text()), self.stuffRatioInputs))
        test = sum(data)
        if self.ratioDialog is None and test != 0:
            self.ratioDialog = RatioDialog(data)
        else:
            if self.ratioDialog is not None:
                self.ratioDialog.close()
            self.ratioDialog = None

    def closeEvent(self, event):
        if self.ratioDialog:
            self.ratioDialog.close()
        if self.settingsDialog:
            self.settingsDialog.close()
    
    def keyPressEvent(self, event):
        # If return button pressed
        if self.selectorWidget.currentIndex() == 1:
            if event.key() == Qt.Key_Return:
                self.searchButton.click()

    def retranslateUi(self):
        self.setWindowTitle('Spoon %s' % self.version)

        self.actions['lockRatio'].setText('비율 바 잠금')
        self.actions['changeMode'].setText('모드 변경 (공사 중)')
        self.actions['settings'].setText('설정')
        self.actions['help'].setText('도움말 (공사 중)')

        self.ratioBox.setTitle('비율')
        
        self.nameRadio.setText('이름')
        self.effectRadio.setText('효과')
        self.stuffRadio.setText('재료')
        self.searchButton.setText('검색')

        for i in range(0, 3):
            self.stuffLabels[i].setText('재료%d' % (i + 1))
            self.stuffLabels[i].setStyleSheet(STYLE_BOLD)
            self.percentLabels[i].setText('%') 

        self.infoBox.setTitle('정보')
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
