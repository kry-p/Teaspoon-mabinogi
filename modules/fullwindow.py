# -*- coding: utf-8 -*-
'''
# Main window for Spoon
# https://github.com/kry-p/Teaspoon-mabinogi
'''

from PyQt5.QtCore import (QCoreApplication, QMetaObject, QRect, QSize,
                            Qt, QEvent)
from PyQt5.QtGui import (QStandardItem, QStandardItemModel)
from PyQt5.QtWidgets import (QComboBox, QGroupBox, QLabel,
                               QListView, QMainWindow, QMenu, QMenuBar,
                               QPushButton, QRadioButton, QSizePolicy,
                               QAction, QTabWidget, QWidget, QStatusBar)
from PyQt5.QtWidgets import QLineEdit

# import time
# import threading

from modules.elements import Widget
from . import database_manager
from .preferences_provider import (preferences, watcher, init, getPreferences)
from .common import Common, customEvent


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
        self.common = Common()
        self.currentFood = getPreferences('currentFood')
        self.favorites = [] if getPreferences('favorites')['item'] is None else getPreferences('favorites')['item']

        # Settings watcher
        watcher.fileChanged.connect(self.onFileChanged)

        # history
        self.history = list()
        self.isInit = True

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
        self.ratioBarButton.clicked.connect(lambda : self.common.toggleRatioDialog(self.stuffRatioInputs))
        self.recipeListView.doubleClicked.connect(self.listAddToFavorites)
        self.searchListView.doubleClicked.connect(self.searchAddToFavorites)
        self.actions['settings'].triggered.connect(self.common.openSettingsDialog)
        self.actions['lockRatio'].triggered.connect(self.toggleRatioBarLocked)
        self.rankComboBox.currentIndexChanged.connect(self.onChangeCategory)
        self.recipeListSelectionModel.currentChanged.connect(
            self.onRecipeListViewValueChanged)
        self.searchListSelectionModel.currentChanged.connect(
            self.onSearchListViewValueChanged)
        self.favoriteListSelectionModel.currentChanged.connect(
            self.onFavoriteListViewValueChanged)

        self.alignUpButton.clicked.connect(self.onChangeFavoriteOrderUp)
        self.alignDownButton.clicked.connect(self.onChangeFavoriteOrderDown)
        self.favoriteDeleteButton.clicked.connect(self.onSelectedFavoriteDeleted)
        self.searchButton.clicked.connect(self.search)
        self.selectorWidget.currentChanged.connect(self.onTabIndexChanged)

        self.actions['changeMode'].triggered.connect(self.onChangeMainDialog)
       
        # Misc. operations
        self.selectorWidget.setCurrentIndex(int(getPreferences('currentTabIndex')))
        if int(getPreferences('currentCategoryItemIndex')) != -1:
            self.recipeListView.setCurrentIndex(self.recipeListModel.index(int(getPreferences('currentCategoryItemIndex')), 0))

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
        if self.common.ratioDialog is not None:
            data = list(map(lambda value: 0 if value.text() ==
                '' else int(value.text()), self.stuffRatioInputs))
            self.common.ratioDialog.update(data)

    """ ********** UI ********** """
    def setWindow(self):
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(520, 364))
        self.setMaximumSize(QSize(520, 364))
        self.setFixedSize(QSize(520, 364))
        self.mainWidget = QWidget(self)
        
        # Status bar
        self.statusBar = QStatusBar(self)
        self.statusBar.setGeometry(QRect(0, 340, 520, 24))

    def createMenuBar(self):
        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 520, 24))
        self.toolsMenu = QMenu(self.menuBar)
        self.toolsMenu.setTitle('도구')
        self.setMenuBar(self.menuBar)
        self.actions = {'lockRatio': QAction(self), 'changeMode': QAction(self),
                        'settings': QAction(self), 'help': QAction(self)}
        self.actions['lockRatio'].setCheckable(True)
        self.actions['lockRatio'].setChecked(
            True if getPreferences('ratioBarLocked') == 'true' else False)
        self.actions['help'].setEnabled(False)

        self.toolsMenu.addAction(self.actions['lockRatio'])
        self.toolsMenu.addAction(self.actions['changeMode'])
        self.toolsMenu.addSeparator()
        self.toolsMenu.addAction(self.actions['settings'])
        self.toolsMenu.addAction(self.actions['help'])

        self.historyMenu = QMenu(self.menuBar)
        self.historyMenu.setTitle('히스토리')

        self.menuBar.addAction(self.toolsMenu.menuAction())
        self.menuBar.addAction(self.historyMenu.menuAction())
        

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
            self.stuffLabels[i].setGeometry(QRect(10, 29 + i * 30, 41, 20))
            self.stuffNames[i].setGeometry(QRect(60, 29 + i * 30, 121, 20))
            self.percentLabels[i].setGeometry(QRect(260, 29 + i * 30, 21, 20))
            self.stuffRatioInputs[i].setGeometry(
                QRect(215, 29 + i * 30, 41, 20))
            self.stuffRatioInputs[i].setAlignment(Qt.AlignRight)
            self.stuffRatioInputs[i].setEnabled(False) 

        customEvent(self.stuffNames[0], QEvent.MouseButtonPress).connect(lambda : self.onRecipeItemClicked(0, 1))
        customEvent(self.stuffNames[1], QEvent.MouseButtonPress).connect(lambda : self.onRecipeItemClicked(1, 1))
        customEvent(self.stuffNames[2], QEvent.MouseButtonPress).connect(lambda : self.onRecipeItemClicked(2, 1))

        customEvent(self.stuffNames[0], QEvent.MouseButtonDblClick).connect(lambda : self.onRecipeItemClicked(0, 2))
        customEvent(self.stuffNames[1], QEvent.MouseButtonDblClick).connect(lambda : self.onRecipeItemClicked(1, 2))
        customEvent(self.stuffNames[2], QEvent.MouseButtonDblClick).connect(lambda : self.onRecipeItemClicked(2, 2))

    def createInfoBox(self):
        self.infoBox = QGroupBox(self.mainWidget)
        self.infoBox.setGeometry(QRect(215, 130, 295, 181))

        self.createChrBox()
        self.createStatBox()
        self.createAtkBox()
        self.createDefBox()

        values = self.statValue + self.defValue + self.atkValue

        for i in values:
            i.getWidget().setAlignment(Qt.AlignRight)

    def createChrBox(self):
        self.chrBox = QGroupBox(self.infoBox)
        self.chrBox.setGeometry(QRect(10, 20, 275, 31))

        self.chrLabel = [        
            Widget(widget = QLabel(self.chrBox), geometry = QRect(10, 6, 31, 16), text = 'HP', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.chrBox), geometry = QRect(105, 6, 31, 16), text = 'MP', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.chrBox), geometry = QRect(200, 6, 31, 16), text = 'SP', stylesheet = STYLE_BOLD)
        ]
        self.chrValue = [
            Widget(widget = QLabel(self.chrBox), geometry = QRect(40, 6, 31, 16)),
            Widget(widget = QLabel(self.chrBox), geometry = QRect(135, 6, 31, 16)),
            Widget(widget = QLabel(self.chrBox), geometry = QRect(230, 6, 31, 16))        
        ]

    def createStatBox(self):
        self.statBox = QGroupBox(self.infoBox)
        self.statBox.setGeometry(QRect(10, 60, 86, 111))

        self.statLabel = [
            Widget(widget = QLabel(self.statBox), geometry = QRect(10, 6, 31, 16), text = '체력', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.statBox), geometry = QRect(10, 26, 31, 16), text = '지력', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.statBox), geometry = QRect(10, 46, 31, 16), text = '솜씨', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.statBox), geometry = QRect(10, 66, 31, 16), text = '의지', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.statBox), geometry = QRect(10, 86, 31, 16), text = '행운', stylesheet = STYLE_BOLD)
        ]
        self.statValue = [
            Widget(widget = QLabel(self.statBox), geometry = QRect(40, 7, 34, 16)),
            Widget(widget = QLabel(self.statBox), geometry = QRect(40, 27, 34, 16)),
            Widget(widget = QLabel(self.statBox), geometry = QRect(40, 47, 34, 16)),
            Widget(widget = QLabel(self.statBox), geometry = QRect(40, 67, 34, 16)),
            Widget(widget = QLabel(self.statBox), geometry = QRect(40, 87, 34, 16)),
        ]

    def createDefBox(self):
        self.defBox = QGroupBox(self.infoBox)
        self.defBox.setGeometry(QRect(105, 60, 85, 111))

        self.defLabel = [
            Widget(widget = QLabel(self.defBox), geometry = QRect(10, 6, 31, 16), text = '방어', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.defBox), geometry = QRect(10, 33, 31, 16), text = '보호', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.defBox), geometry = QRect(10, 59, 31, 16), text = '마방', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.defBox), geometry = QRect(10, 86, 31, 16), text = '마보', stylesheet = STYLE_BOLD),
        ]

        self.defValue = [
            Widget(widget = QLabel(self.defBox), geometry = QRect(40, 7, 34, 16)),
            Widget(widget = QLabel(self.defBox), geometry = QRect(40, 34, 34, 16)),
            Widget(widget = QLabel(self.defBox), geometry = QRect(40, 60, 34, 16)),
            Widget(widget = QLabel(self.defBox), geometry = QRect(40, 87, 34, 16)),
        ]
    
    def createAtkBox(self):
        self.atkBox = QGroupBox(self.infoBox)
        self.atkBox.setGeometry(QRect(199, 60, 86, 111))

        self.atkLabel = [
            Widget(widget = QLabel(self.atkBox), geometry = QRect(10, 6, 31, 16), text = '민댐', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.atkBox), geometry = QRect(10, 33, 31, 16), text = '맥댐', stylesheet = STYLE_BOLD),
            Widget(widget = QLabel(self.atkBox), geometry = QRect(10, 59, 31, 16), text = '마공', stylesheet = STYLE_BOLD),
        ]

        self.atkValue = [
            Widget(widget = QLabel(self.atkBox), geometry = QRect(40, 7, 34, 16)),
            Widget(widget = QLabel(self.atkBox), geometry = QRect(40, 34, 34, 16)),
            Widget(widget = QLabel(self.atkBox), geometry = QRect(40, 60, 34, 16)),
        ]

        self.eftLabel = QLabel(self.atkBox)
        self.eftLabel.setGeometry(QRect(10, 86, 31, 16))
        self.eftValue = Widget(widget = QLabel(self.atkBox), geometry = QRect(40, 86, 34, 16), stylesheet = STYLE_BOLD)
        self.eftValue.getWidget().setAlignment(Qt.AlignCenter)

    """ ---------- Functions ---------- """
    # Set mini window by instance
    def setMiniWindow(self, window):
        self.mini = window

    # When stuff item selected
    def onRecipeItemClicked(self, pos, count):
        text = self.stuffNames[pos].text().replace(' *', '')
        temp = getPreferences('currentFood')

        if count == 1:  # 입수처
            relatedIngredient = db.getRelatedIngredient(text)
            if len(relatedIngredient) == 0:
                self.setStatusBarMessage('%s의 입수처가 없습니다.' % text)
            else:
                relatedIngredient = relatedIngredient[0] 
                # title = '판매처 정보'
                seller = ''
                for i in range(0, 21):
                    if relatedIngredient[i + 4] == 1:
                        seller += CATEGORIES['npcList'][i] + ', '
                seller = seller[:-2]
                self.setStatusBarMessage(text + ' ' + str(relatedIngredient[2]) + 'G : ' + seller)

        if count == 2:  # 점프
            relatedRecipe = db.getRelatedRecipe(text)

            if len(relatedRecipe) != 0:
                relatedRecipe = relatedRecipe[0][0]
                res = self.jumpToFood(relatedRecipe)

                if res == 0:
                    self.setStatusBarMessage('%s의 레시피입니다.' % relatedRecipe)
                else:
                    self.setStatusBarMessage('%s와(과) 연관된 레시피가 없습니다.' % text)
    
    # Left tab index
    def onTabIndexChanged(self):
        preferences.setValue('currentTabIndex', self.selectorWidget.currentIndex())

    # Search
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
                query = list()
                categories = ["체력", "지력", "솜씨", "의지", "행운",
                              "HP", "MP", "SP",
                              "민댐", "맥댐", "마공",
                              "방어", "보호", "마방", "마보", "효과"]
                text = [item for item in currentText.split(' ') if item != '']
                try:
                    for i in range(len(text)):
                        if i % 2 == 1:
                            oper = text[i]
                            if oper.lower() == 'and' or oper.lower() == 'or':
                                query.append(oper.upper())
                            else:
                                raise Exception
                        else:
                            query.append(CATEGORIES['effectColumns'][15 - categories.index(text[i])])
                    if len(query) % 2 == 0:
                        raise Exception
                    result = db.searchByEffect(query)
                    self.setStatusBarMessage('')
                except:
                    self.setStatusBarMessage('검색어를 잘못 입력했습니다. 정확하게 입력했는지 확인해 주세요.')
            if currentEnabled == 2:
                try:
                    result = db.searchByIngredient(currentText)
                except:
                    result = None
            if result is not None:
                for item in result:
                    currentItem = QStandardItem(item[0] + (' *' if item[1] == 1 else ''))
                    currentItem.setEditable(False)
                    self.searchListModel.appendRow(currentItem)
    
    # Set status bar message
    def setStatusBarMessage(self, message):
        # Display message for 10 sec.
        self.statusBar.showMessage(message, 10000)
        
    def jumpToFood(self, food):
        self.setFoodInfo(food)
        rank = db.getRank(food)

        if rank != -1:
            recipes = db.getFoods(rank)
            if len(recipes) != 0:  # Gets list of foods
                recipes = list(zip(*recipes))[0]
                self.rankComboBox.setCurrentIndex(CATEGORIES['categoryCode'].index(rank))  # set combo box idx
                self.recipeListView.setCurrentIndex(self.recipeListModel.index(recipes.index(food), 0))  # set list idx
            return 0
        else:
            return -1

    """ ----------- Actions ----------- """
    def getCurrentCategoryList(self):
        self.recipeListModel.clear()
        currentCategoryItems = db.getFoods(
            CATEGORIES['categoryCode'][self.rankComboBox.currentIndex()])

        for item in currentCategoryItems:
            currentItem = QStandardItem(item[0] + (' *' if item[1] == 1 else ''))
            currentItem.setEditable(False)
            self.recipeListModel.appendRow(currentItem)

    def onHistoryAdded(self, food):
        def trigger(action, index):
            def run():
                self.setStatusBarMessage('%s의 레시피입니다.' % self.history[index])
                self.jumpToFood(self.history[index])
            action.triggered.connect(lambda : run())

        if self.isInit:
            self.isInit = False
            self.historyMenu.clear()
            emptyAction = Widget(widget = QAction(self), text = '비어 있음', isEnabled = False)
            self.historyMenu.addAction(emptyAction.getWidget())
        else:    
            self.historyMenu.clear()  
            
            if food not in self.history:
                self.history.append(food)
            else:
                # move to head
                self.history.remove(food)
                self.history.append(food)

            self.history.reverse()

            if len(self.history) > 10:
                self.history.remove(self.history[0])
            actions = list()
            for i in range(len(self.history)):
                action = QAction(self)
                action.setText(self.history[i])
                action.setEnabled(True)
                actions.append(action)
                self.historyMenu.addAction(actions[i])
                trigger(actions[i], i)        
        
        

    def setFoodInfo(self, foodName):
        statValues = self.statValue + self.chrValue\
                + self.atkValue + self.defValue
        info = db.getFoodInfo(foodName)
        ingredients = info['ingredients'][0]
        ratio = info['ratio'][0]
        special = info['specialEffects'][0]
        stats = info['stats'][0]
        isRelated = list()

        for ingredient in ingredients:            
            if ingredient is None:
                isRelated.append(None)
            else:
                related = db.getRelatedRecipe(ingredient)
                if len(related) > 0:
                    isRelated.append(related[0][0])
                else:
                    isRelated.append(None)

        for i in range(0, 3):
            if ingredients[i] is None:
                self.stuffNames[i].setText('')
                self.stuffRatioInputs[i].setText('')
            else:
                self.stuffNames[i].setText(ingredients[i])
                self.stuffRatioInputs[i].setText(str(int(ratio[i])))
                if isRelated[i] is None:
                    self.stuffNames[i].setStyleSheet('')
                else:
                    self.stuffNames[i].setStyleSheet('text-decoration: underline;')

        self.eftValue.getWidget().setText('' if special[0] is None else special[0])
        self.eftValue.getWidget().setToolTip('효과 없음' if special[1] is None else special[1])

        for idx in range(len(statValues)):
            val = stats[idx]

            statValues[idx].setText('' if stats[idx] is None else str(int(stats[idx])))
            
            if val is not None and int(val) > 0:
                statValues[idx].setStyleSheet('color: %s;' % COLOR_POSITIVE)
            else:
                statValues[idx].setStyleSheet('color: %s;' % COLOR_NEGATIVE)

    def onChangeMainDialog(self):
        self.mini.show()
        self.close()

    # UI elements
    def toggleRatioBarLocked(self):
        preferences.setValue('ratioBarLocked',
                            self.actions['lockRatio'].isChecked())

    # Categories
    def onChangeCategory(self):
        preferences.setValue('currentCategoryIndex',
                          self.rankComboBox.currentIndex())
        self.getCurrentCategoryList()
        preferences.setValue('currentCategoryItemIndex', -1)

    def onRecipeListViewValueChanged(self):
        currentIndex = self.recipeListSelectionModel.currentIndex().row()

        if currentIndex != -1:
            currentFood = self.recipeListModel.item(currentIndex, 0).text().replace(' *', '')
            preferences.setValue('currentFood', currentFood)
            preferences.setValue('currentCategoryItemIndex', currentIndex)
            self.setFoodInfo(currentFood)
            self.onHistoryAdded(currentFood)

    # Search
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
            self.setStatusBarMessage('즐겨찾기에 %s 요리가 추가되었습니다.' % selected)

    def onSearchListViewValueChanged(self):
        currentIndex = self.searchListSelectionModel.currentIndex().row()
        if currentIndex != -1:
            currentFood = self.searchListModel.item(currentIndex, 0).text().replace(' *', '')
            preferences.setValue(
                'currentFood', currentFood)
            self.setFoodInfo(currentFood)
            self.onHistoryAdded(currentFood)

    # Favorites
    def listAddToFavorites(self):
        preferences.setValue('currentFavoritesIndex', -1)
        currentIndex = self.recipeListSelectionModel.currentIndex().row()
        if currentIndex != -1:
            selected = self.recipeListModel.item(currentIndex, 0).text()
            self.favorites.append(selected)
            self.favorites = list(dict.fromkeys(self.favorites))
            preferences.setValue('favorites', {'item': self.favorites})
            self.updateFavoriteList()
            self.setStatusBarMessage('즐겨찾기에 %s 요리가 추가되었습니다.' % selected)

    def onFavoriteListViewValueChanged(self):
        currentIndex = self.favoriteListSelectionModel.currentIndex().row()
        if currentIndex != -1:
            currentFood = self.favoriteListModel.item(currentIndex, 0).text().replace(' *', '')
            preferences.setValue(
                'currentFood', currentFood)
            self.setFoodInfo(currentFood)
            self.onHistoryAdded(currentFood)

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
            preferences.setValue('currentFavoritesIndex', currentPos)

    def onChangeFavoriteOrderDown(self):
        currentPos = self.favoriteListSelectionModel.currentIndex().row()

        if currentPos != -1 and currentPos < (len(self.favorites) - 1):
            temp = self.favorites[currentPos + 1]
            self.favorites[currentPos + 1] = self.favorites[currentPos]
            self.favorites[currentPos] = temp
            self.updateFavoriteList()
            self.favoriteListView.setCurrentIndex(self.favoriteListViewModel.index(currentPos + 1, 0))
            preferences.setValue('currentFavoritesIndex', currentPos)

    def onSelectedFavoriteDeleted(self):
        currentPos = self.favoriteListSelectionModel.currentIndex().row()
        if currentPos != -1:
            currentFood = self.favoriteListModel.item(currentPos, 0).text()
            self.favorites.pop(currentPos)
            self.updateFavoriteList()
            preferences.setValue('favorites', {
                'item': self.favorites
            })
            preferences.setValue('currentFavoritesIndex', -1)
            self.setStatusBarMessage('%s 요리가 즐겨찾기에서 삭제되었습니다.' % currentFood)
           
    """ ----------- Events ----------- """
    def closeEvent(self, event):
        if self.common.ratioDialog:
            self.common.ratioDialog.close()
        if self.common.settingsDialog:
            self.common.settingsDialog.close()

    def keyPressEvent(self, event):
        if self.selectorWidget.currentIndex() == 1:
            if event.key() == Qt.Key_Return:
                self.searchButton.click()

    """ -------- Translations -------- """
    def retranslateUi(self):
        self.setWindowTitle('Spoon %s' % self.version)

        self.actions['lockRatio'].setText('비율 바 잠금')
        self.actions['changeMode'].setText('모드 변경')
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
        

