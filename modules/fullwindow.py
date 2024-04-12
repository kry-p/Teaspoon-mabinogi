# -*- coding: utf-8 -*-
'''
# Main window for Spoon
# https://github.com/kry-p/Teaspoon-mabinogi
'''
import math
import re
from enum import Enum
from PyQt5.QtCore import (QMetaObject, QRect, QSize, Qt, QEvent)
from PyQt5.QtGui import (QStandardItem, QStandardItemModel)
from PyQt5.QtWidgets import (QComboBox, QGroupBox, QLabel,
                               QListView, QMainWindow, QMenu, QMenuBar,
                               QPushButton, QRadioButton, QSizePolicy,
                               QAction, QTabWidget, QWidget, QStatusBar)
from PyQt5.QtWidgets import QLineEdit
from modules.elements import Widget
from .database_manager import DBManager
from .preferences_provider import (preferences, watcher, getPreferences)
from .common import (Common, customEvent)

db = DBManager()
CATEGORIES = db.getCategories()
COLOR_POSITIVE = '#0099FF'
COLOR_NEGATIVE = '#FF0000'
STYLE_BOLD = 'font-weight: 600;'
WINDOW_WIDTH = 520
WINDOW_HEIGHT = 364

class ChangeOrderType(Enum):
    UP = 1
    DOWN = -1

# Main window (Full)
class FullWindow(QMainWindow):
    def __init__(self, version : str, resources) -> None:
        super().__init__()

        self.version = version
        self.common = Common(resources)
        self.currentFood = getPreferences('currentFood')
        favorites = getPreferences('favorites')
        # Validates favorites dictionary before use
        self.favorites = [] if type(favorites) != "<class 'dict'>" or 'item' in favorites == false else getPreferences('favorites')['item']

        # Settings watcher
        watcher.fileChanged.connect(self.fileChangeEvent)

        # history
        self.history = list()
        self.isInit = True

        self.setWindow()  # Settings for window
        self.createMenuBar()  # Menu bar
        self.createStuffBox()  # Stuff ratio box
        self.createInfoBox()  # Information box
        self.createLeftToolBox()  # Left toolbox

        ''' Misc. buttons '''
        self.ratioBarButton = QPushButton(self.mainWidget)
        self.ratioBarButton.setGeometry(QRect(9, 280, 201, 31))

        self.setCentralWidget(self.mainWidget)
        self.selectorWidget.setCurrentIndex(0)

        ''' Actions '''
        # buttons
        self.ratioBarButton.clicked.connect(lambda : self.common.toggleRatioDialog(self.stuffRatioInputs))
        self.alignUpButton.clicked.connect(lambda : self.changeFavoriteOrder(ChangeOrderType.UP))
        self.alignDownButton.clicked.connect(lambda : self.changeFavoriteOrder(ChangeOrderType.DOWN))
        self.favoriteDeleteButton.clicked.connect(self.deleteSelectedFavorite)
        self.searchButton.clicked.connect(self.search)
        
        # listview items
        self.recipeListView.doubleClicked.connect(self.addFavoriteFromRecipe)
        self.searchListView.doubleClicked.connect(self.addFavoriteFromSearch)
        self.recipeListSelectionModel.currentChanged.connect(
            self.changeRecipeListViewValue)
        self.searchListSelectionModel.currentChanged.connect(
            self.changeSearchListViewValue)
        self.favoriteListSelectionModel.currentChanged.connect(
            self.changeCurrentRecipeByFavorite)

        # combo box
        self.rankComboBox.currentIndexChanged.connect(self.changeCategory)
        
        # left tab
        self.selectorWidget.currentChanged.connect(self.changeTabIndex)

        # actions
        self.actions['settings'].triggered.connect(self.common.openSettingsDialog)
        self.actions['lockRatio'].triggered.connect(self.toggleRatioBarLocked)
        self.actions['changeMode'].triggered.connect(self.changeMainDialog)
        self.actions['help'].triggered.connect(self.common.openHelpDialog)
       
        ''' Misc. operations '''
        self.selectorWidget.setCurrentIndex(int(getPreferences('currentTabIndex')))
        if int(getPreferences('currentCategoryItemIndex')) != -1:
            self.recipeListView.setCurrentIndex(self.recipeListModel.index(int(getPreferences('currentCategoryItemIndex')), 0))

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    """ ********** UI ********** """
    def setWindow(self) -> None:
        self.setWindowTitle('Spoon %s' % self.version)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setSizePolicy(sizePolicy)
        self.setFixedSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.mainWidget = QWidget(self)
        
        # Status bar
        self.statusBar = QStatusBar(self)
        self.statusBar.setGeometry(QRect(0, 340, 520, 24))

    def createMenuBar(self) -> None:
        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 520, 24))
        self.setMenuBar(self.menuBar)
  
        self.toolsMenu = QMenu(self.menuBar)
        self.toolsMenu.setTitle('도구')
  
        self.actions = {'lockRatio': QAction(self), 'changeMode': QAction(self),
                        'settings': QAction(self), 'help': QAction(self)}
        self.actions['lockRatio'].setCheckable(True)
        self.actions['lockRatio'].setChecked(
            True if getPreferences('ratioBarLocked') == 'true' else False)
        # self.actions['help'].setEnabled(False)

        self.toolsMenu.addAction(self.actions['lockRatio'])
        self.toolsMenu.addAction(self.actions['changeMode'])
        self.toolsMenu.addSeparator()
        self.toolsMenu.addAction(self.actions['settings'])
        self.toolsMenu.addAction(self.actions['help'])

        self.historyMenu = QMenu(self.menuBar)
        self.historyMenu.setTitle('히스토리')
        self.dummyAction = QAction()
        self.dummyAction.setEnabled(False)
        self.dummyAction.setText('(비어 있음)')

        self.historyMenu.addAction(self.dummyAction)

        self.menuBar.addAction(self.historyMenu.menuAction())
        self.menuBar.addAction(self.toolsMenu.menuAction())        

    def createLeftToolBox(self) -> None:
        self.selectorWidget = QTabWidget(self.mainWidget)
        self.selectorWidget.setGeometry(QRect(10, 10, 201, 271))

        self.recipeListMenu = QWidget()
        self.searchMenu = QWidget()
        self.favoriteMenu = QWidget()

        self.createLeftFirstTab()
        self.createLeftSecondTab()
        self.createLeftThirdTab()

    def createLeftFirstTab(self) -> None:
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
        if self.currentFood != '' and self.currentFood is not None:
            self.setFoodInfo(self.currentFood)

    def createLeftSecondTab(self) -> None:
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

    def createLeftThirdTab(self) -> None:
        self.favoriteListView = QListView(self.favoriteMenu)
        self.favoriteListView.setGeometry(QRect(12, 10, 171, 195))
        self.favoriteListModel = QStandardItemModel()
        self.favoriteListView.setModel(self.favoriteListModel)
        self.favoriteListSelectionModel = self.favoriteListView.selectionModel()
        self.favoriteListViewModel = self.favoriteListView.model()

        self.updateFavorite()

        self.alignUpButton = QPushButton(self.favoriteMenu)
        self.alignUpButton.setGeometry(QRect(11, 210, 31, 23))
        self.alignDownButton = QPushButton(self.favoriteMenu)
        self.alignDownButton.setGeometry(QRect(39, 210, 31, 23))
        self.favoriteDeleteButton = QPushButton(self.favoriteMenu)
        self.favoriteDeleteButton.setGeometry(QRect(132, 210, 51, 23))

        self.selectorWidget.addTab(self.recipeListMenu, '')
        self.selectorWidget.addTab(self.searchMenu, '')
        self.selectorWidget.addTab(self.favoriteMenu, '')

    def createStuffBox(self) -> None:
        def createClickEvent(widget, idx : int) -> None:
            customEvent(widget, QEvent.MouseButtonPress).connect(lambda : self.recipeItemClicked(idx, 1))
            customEvent(widget, QEvent.MouseButtonDblClick).connect(lambda : self.recipeItemClicked(idx, 2))

        self.ratioBox = QGroupBox(self.mainWidget)
        self.ratioBox.setGeometry(QRect(215, 10, 295, 121))
        self.stuffLabels = list()
        self.stuffNames = list()
        self.percentLabels = list()
        self.stuffRatioInputs = list()

        for i in range(3):
            self.stuffLabels.append(QLabel(self.ratioBox))
            self.stuffNames.append(QLabel(self.ratioBox))
            self.percentLabels.append(QLabel(self.ratioBox))
            self.stuffRatioInputs.append(QLineEdit(self.ratioBox))
            self.stuffLabels[i].setGeometry(QRect(10, 29 + i * 30, 41, 20))
            self.stuffNames[i].setGeometry(QRect(60, 29 + i * 30, 121, 20))
            self.percentLabels[i].setGeometry(QRect(260, 29 + i * 30, 21, 20))
            self.stuffRatioInputs[i].setGeometry(
                QRect(215, 29 + i * 30, 41, 20))
            self.stuffRatioInputs[i].setAlignment(Qt.AlignRight)
            self.stuffRatioInputs[i].setEnabled(False) 

        for i in range(0, 3):
            self.stuffLabels[i].setText('재료%d' % (i + 1))
            self.stuffLabels[i].setStyleSheet(STYLE_BOLD)
            self.percentLabels[i].setText('%') 

        for idx in range(3):
            createClickEvent(self.stuffNames[idx], idx)

    def createInfoBox(self) -> None:
        self.infoBox = QGroupBox(self.mainWidget)
        self.infoBox.setGeometry(QRect(215, 130, 295, 181))

        self.createChrBox()
        self.createStatBox()
        self.createAtkBox()
        self.createDefBox()

        values = self.statValue + self.defValue + self.atkValue

        for i in values:
            i.getWidget().setAlignment(Qt.AlignRight)

    def createChrBox(self) -> None:
        self.chrBox = QGroupBox(self.infoBox)
        self.chrBox.setGeometry(QRect(10, 20, 275, 31))
        self.chrText = ['HP', 'MP', 'SP']
        self.chrLabel = list()
        self.chrValue = list()

        for i in range(3):
            self.chrLabel.append(Widget(widget = QLabel(self.chrBox), geometry = QRect(10 + 95 * i, 6, 31, 16), text = self.chrText[i], stylesheet = STYLE_BOLD))
            self.chrValue.append(Widget(widget = QLabel(self.chrBox), geometry = QRect(40 + 95 * i, 6, 31, 16)))

    def createStatBox(self) -> None:
        self.statBox = QGroupBox(self.infoBox)
        self.statBox.setGeometry(QRect(10, 60, 86, 111))

        self.statText = ['체력', '지력', '솜씨', '의지', '행운']
        self.statLabel = list()
        self.statValue = list()
        for i in range(5):
            self.statLabel.append(Widget(widget = QLabel(self.statBox), geometry = QRect(10, 6 + 20 * i, 31, 16),
                                         text = self.statText[i], stylesheet = STYLE_BOLD))
            self.statValue.append(Widget(widget = QLabel(self.statBox), geometry = QRect(40, 7 + 20 * i, 34, 16)))

    def createDefBox(self) -> None:
        self.defBox = QGroupBox(self.infoBox)
        self.defBox.setGeometry(QRect(105, 60, 85, 111))

        self.defText = ['방어', '보호', '마방', '마보']
        self.defLabel = list()
        self.defValue = list()
        for i in range(4):
            self.defLabel.append(Widget(widget = QLabel(self.defBox), geometry = QRect(10, math.ceil(6 + 26.5 * i), 31, 16),
                                         text = self.defText[i], stylesheet = STYLE_BOLD))
            self.defValue.append(Widget(widget = QLabel(self.defBox), geometry = QRect(40, math.ceil(7 + 26.5 * i), 34, 16)))

    def createAtkBox(self) -> None:
        self.atkBox = QGroupBox(self.infoBox)
        self.atkBox.setGeometry(QRect(199, 60, 86, 111))
        self.atkText = ['민댐', '맥댐', '마공']
        self.atkLabel = list()
        self.atkValue = list()

        for i in range(3):
            self.atkLabel.append(Widget(widget = QLabel(self.atkBox), geometry = QRect(10, math.ceil(6 + 26.5 * i), 31, 16), text = self.atkText[i], stylesheet = STYLE_BOLD))
            self.atkValue.append(Widget(widget = QLabel(self.atkBox), geometry = QRect(40, math.ceil(7 + 26.5 * i), 34, 16)))

        self.eftLabel = QLabel(self.atkBox)
        self.eftLabel.setGeometry(QRect(10, 86, 31, 16))
        self.eftValue = Widget(widget = QLabel(self.atkBox), geometry = QRect(40, 86, 34, 16), stylesheet = STYLE_BOLD)
        self.eftValue.getWidget().setAlignment(Qt.AlignCenter)

    """ ---------- Functions ---------- """
    ''' Window '''
    # Set mini window by instance
    def setMiniWindow(self, window : QWidget) -> None:
        self.mini = window

    # to mini window
    def changeMainDialog(self) -> None:
        self.mini.show()
        self.close()

    # Left tab index
    def changeTabIndex(self) -> None:
        preferences.setValue('currentTabIndex', self.selectorWidget.currentIndex())

    # Set status bar message
    def setStatusBarMessage(self, message : str) -> None:
        # Display message for 10 sec.
        self.statusBar.showMessage(message, 10000)

    ''' Current recipe '''
    # Jump to specific recipe
    def jumpToFood(self, food : str) -> int:
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
    
    # When stuff item selected
    def recipeItemClicked(self, pos : int, count : int) -> None:
        text = self.stuffNames[pos].text().replace(' *', '')

        if count == 1:  # 입수처
            relatedIngredient = db.getRelatedIngredient(text)
            if len(relatedIngredient) == 0:
                if text != '':
                    self.setStatusBarMessage('%s의 입수처 정보가 없습니다.' % text)
            else:
                relatedIngredient = relatedIngredient[0] 
          
                seller = ''
                for i in range(0, len(CATEGORIES['npcList'])):
                    if relatedIngredient[i + 4] == 1:
                        seller += CATEGORIES['npcList'][i] + ', '
                seller = seller[:-2]
                cost = relatedIngredient[2]

                if cost == 0:
                    self.setStatusBarMessage(text + ' - 가격 정보 없음 : ' + seller)
                else:
                    self.setStatusBarMessage(text + ' ' + str(relatedIngredient[2]) + 'G : ' + seller)

        if count == 2:  # 점프
            relatedRecipe = db.getRelatedRecipe(text)

            if len(relatedRecipe) != 0:
                relatedRecipe = relatedRecipe[0][0]
                res = self.jumpToFood(relatedRecipe)

                if res == 0:
                    self.setStatusBarMessage('%s의 레시피입니다.' % relatedRecipe)
                else:
                    if text != '':
                        self.setStatusBarMessage('%s와(과) 연관된 레시피가 없습니다.' % text)

    ''' Recipes tab '''
    # Change recipe tab categories
    def changeCategory(self) -> None:
        preferences.setValue('currentCategoryIndex',
                          self.rankComboBox.currentIndex())
        self.getCurrentCategoryList()
        preferences.setValue('currentCategoryItemIndex', -1)

    # Get current category's list of recipes
    def getCurrentCategoryList(self) -> None:
        self.recipeListModel.clear()
        currentCategoryItems = db.getFoods(
            CATEGORIES['categoryCode'][self.rankComboBox.currentIndex()])

        for item in currentCategoryItems:
            currentItem = QStandardItem(item[0] + (' *' if item[1] == 1 else ''))
            currentItem.setEditable(False)
            self.recipeListModel.appendRow(currentItem)
    
    # On change recipe
    def changeRecipeListViewValue(self) -> None:
        currentIndex = self.recipeListSelectionModel.currentIndex().row()

        if currentIndex != -1:
            currentFood = self.recipeListModel.item(currentIndex, 0).text().replace(' *', '')
            preferences.setValue('currentFood', currentFood)
            preferences.setValue('currentCategoryItemIndex', currentIndex)
            self.setFoodInfo(currentFood)
            self.addToHistory(currentFood)
    
    ''' Search tab '''
    # Search
    def search(self) -> None:
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
                categoryCol = list(reversed(CATEGORIES['effectColumns']))
                query = dict()
                
                def syntaxErrorChecker(queryItems : list):
                    logic = list()
                    for item in text:
                        if item.lower() == 'and' or item.lower() == 'or':
                            # put in logical operation string (upper case)
                            logic.append(text.pop(text.index(item)).upper())  

                    query['logic'] = logic
                    # unknown categories
                    for item in queryItems:
                        if not item.isdigit() and item not in categories:
                            return False

                    # numbers
                    numberCount = 0
                    for i in range(len(queryItems)):
                        if queryItems[i].isdigit():
                            numberCount += 1
                        else:
                            if numberCount != 0 and numberCount != 2:
                                return False
                            if i != 0:
                                query[categoryCol[categories.index(queryItems[i - numberCount - 1])]] = queryItems[i - numberCount : i]
                            numberCount = 0
                        if i == len(queryItems) - 1:
                            if numberCount != 0 and numberCount != 2:
                                return False
                            query[categoryCol[categories.index(queryItems[(i - numberCount)])]] = queryItems[i - numberCount + 1 : i + 1]
                    
                    if len(query) - len(query['logic']) == 2:
                        return True
                    else:
                        return False
            
                text = [item for item in re.split(r'[ ~]', currentText) if item != '']

                if syntaxErrorChecker(text):
                    result = db.searchByEffect(query)
                    self.setStatusBarMessage('')
                else:
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

    # Search -> Favorite
    def addFavoriteFromSearch(self) -> None:
        currentIndex = self.searchListSelectionModel.currentIndex().row()
        if currentIndex != -1:
            selected = self.searchListModel.item(currentIndex, 0).text()
            self.favorites.append(selected)
            self.favorites = list(dict.fromkeys(self.favorites))
            preferences.setValue('favorites', {
                'item': self.favorites
            })
            self.updateFavorite()
            self.setStatusBarMessage('즐겨찾기에 %s 요리가 추가되었습니다.' % selected)

    # On change value of search results
    def changeSearchListViewValue(self) -> None:
        currentIndex = self.searchListSelectionModel.currentIndex().row()
        if currentIndex != -1:
            currentFood = self.searchListModel.item(currentIndex, 0).text().replace(' *', '')
            preferences.setValue(
                'currentFood', currentFood)
            self.setFoodInfo(currentFood)
            self.addToHistory(currentFood)

    ''' Favorites tab '''
    # Add
    def addFavoriteFromRecipe(self) -> None:
        preferences.setValue('currentFavoritesIndex', -1)
        currentIndex = self.recipeListSelectionModel.currentIndex().row()
        if currentIndex != -1:
            selected = self.recipeListModel.item(currentIndex, 0).text()
            self.favorites.append(selected)
            self.favorites = list(dict.fromkeys(self.favorites))
            preferences.setValue('favorites', {'item': self.favorites})
            self.updateFavorite()
            self.setStatusBarMessage('즐겨찾기에 %s 요리가 추가되었습니다.' % selected)

    # Set current recipe by favorites list
    def changeCurrentRecipeByFavorite(self) -> None:
        currentIndex = self.favoriteListSelectionModel.currentIndex().row()
        if currentIndex != -1:
            currentFood = self.favoriteListModel.item(currentIndex, 0).text().replace(' *', '')
            preferences.setValue(
                'currentFood', currentFood)
            self.setFoodInfo(currentFood)
            self.addToHistory(currentFood)

    # Update favorites
    def updateFavorite(self) -> None:
        self.favoriteListModel.clear()

        if self.favorites is not None:
            for item in self.favorites:
                currentItem = QStandardItem(item)
                currentItem.setEditable(False)
                self.favoriteListModel.appendRow(currentItem)

    # Change order of favorite item
    def changeFavoriteOrder(self, direction : ChangeOrderType) -> None:
        currentPos = self.favoriteListSelectionModel.currentIndex().row()
        flag = False
        if direction == ChangeOrderType.UP and currentPos > 0:
            flag = True
            temp = self.favorites[currentPos - 1]
            self.favorites[currentPos - 1] = self.favorites[currentPos]
        elif direction == ChangeOrderType.DOWN and currentPos != -1 and currentPos < (len(self.favorites) - 1):
            flag = True
            temp = self.favorites[currentPos + 1]
            self.favorites[currentPos + 1] = self.favorites[currentPos]
        if flag:
            self.favorites[currentPos] = temp
            self.updateFavorite()
            if direction == ChangeOrderType.UP:        
                self.favoriteListView.setCurrentIndex(self.favoriteListViewModel.index(currentPos - 1, 0))
            else:
                self.favoriteListView.setCurrentIndex(self.favoriteListViewModel.index(currentPos + 1, 0))
            preferences.setValue('currentFavoritesIndex', currentPos)

    # Delete from favorites
    def deleteSelectedFavorite(self) -> None:
        currentPos = self.favoriteListSelectionModel.currentIndex().row()
        if currentPos != -1:
            currentFood = self.favoriteListModel.item(currentPos, 0).text()
            self.favorites.pop(currentPos)
            self.updateFavorite()
            preferences.setValue('favorites', {
                'item': self.favorites
            })
            preferences.setValue('currentFavoritesIndex', -1)
            self.setStatusBarMessage('%s 요리가 즐겨찾기에서 삭제되었습니다.' % currentFood)

    ''' Misc '''
    def addToHistory(self, food : str) -> None:
        def trigger(action, index : int) -> None:
            def run(action, index):
                self.setStatusBarMessage('%s의 레시피입니다.' % action.text())
                self.jumpToFood(self.history[self.history.index(action.text())])
            action.triggered.connect(lambda : run(action, index))

        if self.isInit:
            self.isInit = False
        else:    
            self.historyMenu.clear()  
            
            if food not in self.history:
                self.history.append(food)
            else:
                # move to head
                self.history.remove(food)
                self.history.append(food)

            if len(self.history) > 10:
                self.history.remove(self.history[0])
            actions = list()
            for i in reversed(range(len(self.history))):
                action = QAction(self)
                action.setText(self.history[i])
                action.setEnabled(True)
                actions.append(action)

            for i in range(len(actions)):
                self.historyMenu.addAction(actions[i])
                trigger(actions[i], i)     
        
    def setFoodInfo(self, foodName : str) -> None:
        statValues = self.statValue + self.chrValue\
                + self.atkValue + self.defValue
        info = db.getFoodInfo(foodName)
        rank = db.getRank(foodName)
        ingredients = info['ingredients'][0]
        ratio = info['ratio'][0]
        special = info['specialEffects'][0]
        stats = info['stats'][0]
        rankString = CATEGORIES['categoryName'][CATEGORIES['categoryCode'].index(rank)]
        isRelated = list()

        self.ratioBox.setTitle(foodName + ' : ' + rankString + '  ')

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

        eftValue = ''
        eftTooltip = ''
        divider = int(len(special) / 2)

        for i in range(0, divider):
            if special[i] is not None:
                if i == divider - 1:
                    eftValue += ', %s' % special[i]
                    eftTooltip += ', %s' % special[i + divider]
                elif i == 0:
                    eftValue += '%s' % special[i]
                    eftTooltip += '%s' % special[i + divider]
                else:
                    eftValue += ', %s' % special[i]
                    eftTooltip += ', %s' % special[i + divider]

        self.eftValue.getWidget().setText(eftValue)
        self.eftValue.getWidget().setToolTip('효과 없음' if special[0] is None else eftTooltip)

        for idx in range(len(statValues)):
            val = stats[idx]
            statValues[idx].setText('' if stats[idx] == 0 else str(int(stats[idx])))
            
            if val is not None:
                if int(val) > 0:
                    statValues[idx].setStyleSheet('color: %s;' % COLOR_POSITIVE)
                elif int(val) < 0:
                    statValues[idx].setStyleSheet('color: %s;' % COLOR_NEGATIVE)

    # UI elements
    def toggleRatioBarLocked(self) -> None:
        preferences.setValue('ratioBarLocked',
                            self.actions['lockRatio'].isChecked())

    """ ----------- Events ----------- """
    # If QSettings file has changed
    def fileChangeEvent(self) -> None:
        # Detects favorite 
        favorites = getPreferences('favorites')
        # Validate if favorites setting is valid
        items = [] if type(favorites) != "<class 'dict'>" or 'item' in favorites == false else getPreferences('favorites')['item']

        if items is not None:
            if len(favorites) == 0:
                self.favorites = []
                self.updateFavorite()
        if self.common.ratioDialog is not None and self.isVisible():
            self.common.updateRatioDialog(self.stuffRatioInputs)

    # If close button clicked
    def closeEvent(self, event : QEvent) -> None:
        if self.common.ratioDialog:
            self.common.ratioDialog.close()
        if self.common.settingsDialog:
            self.common.settingsDialog.close()
        if self.common.helpDialog:
            self.common.helpDialog.close()

    # Keyboard listener
    def keyPressEvent(self, event : QEvent) -> None:
        if self.selectorWidget.currentIndex() and event.key() == Qt.Key_Return:
            self.searchButton.click()

    """ -------- Translations -------- """
    # const
    def retranslateUi(self) -> None:
        self.actions['lockRatio'].setText('비율 바 잠금')
        self.actions['changeMode'].setText('모드 변경')
        self.actions['settings'].setText('설정')
        self.actions['help'].setText('도움말')

        self.ratioBox.setTitle('비율')
        
        self.nameRadio.setText('이름')
        self.effectRadio.setText('효과')
        self.stuffRadio.setText('재료')
        self.searchButton.setText('검색')

        self.infoBox.setTitle('정보')
        self.eftLabel.setText('효과')
        self.eftLabel.setStyleSheet(STYLE_BOLD)

        self.selectorWidget.setTabText(self.selectorWidget.indexOf(
            self.recipeListMenu), '목록')
        self.selectorWidget.setTabText(self.selectorWidget.indexOf(
            self.searchMenu), '검색')
        self.selectorWidget.setTabText(self.selectorWidget.indexOf(
            self.favoriteMenu), u'\u2606')

        self.alignUpButton.setText(u'\u25b3')
        self.alignDownButton.setText(u'\u25bd')
        self.favoriteDeleteButton.setText('삭제')

        self.ratioBarButton.setText('비율 바 On / Off')
        