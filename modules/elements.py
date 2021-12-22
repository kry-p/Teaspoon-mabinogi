# -*- coding: utf-8 -*-

class Label():
    def __init__(self, label, geometry, text):
        self.__label = label
        self.__label.setGeometry(geometry)
        self.__label.setText(text)

    def setStyle(self, style):
        self.__label.setStyleSheet(style)

    def getLabel(self):
        return self.__label

class Button():
    def __init__(self, button, geometry, text):
        self.__button = button
        self.__button.setGeometry(geometry)
        self.__button.setText(text)

    def setAction(self, action):
        self.__button.clicked.connect(action)

    def getButton(self):
        return self.__button

class LineEdit():
    def __init__(self, lineEdit, geometry, defaultValue):
        self.__lineEdit = lineEdit
        self.__lineEdit.setGeometry(geometry)
        self.__lineEdit.setText(defaultValue)

    def setTextChangedAction(self, action):
        self.__lineEdit.textChanged.connect(action)

    def setValidator(self, validator):
        self.__lineEdit.setValidator(validator)

    def setText(self, text):
        self.__lineEdit.setText(text)

    def getText(self):
        return self.__lineEdit.text()

    def getInput(self):
        return self.__lineEdit
