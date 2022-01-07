# -*- coding: utf-8 -*-
'''
# QWidget wrapper class for Spoon
# https://github.com/kry-p/Teaspoon-mabinogi
'''
class Widget():
    def __init__(self, **kwargs):
        self.prop = kwargs
        self.widget = self.prop['widget']

        if "geometry" in kwargs:
            self.widget.setGeometry(self.prop['geometry'])
        if "text" in kwargs:
            self.widget.setText(self.prop['text'])
        if "title" in kwargs:
            self.widget.setTitle(self.prop['title'])
        if "isEnabled" in kwargs:
            self.widget.setEnabled(self.prop['isEnabled'])

        if "stylesheet" in kwargs:
            self.widget.setStyleSheet(self.prop['stylesheet'])
        if "onTextChanged" in kwargs:
            self.widget.textChanged.connect(self.prop['onTextChanged'])
        if "validator" in kwargs:
            self.widget.setValidator(self.prop['validator'])
        if "inputMask" in kwargs:
            self.widget.setInputMask(self.prop['inputMask'])
        if "onClick" in kwargs:
            self.widget.clicked.connect(self.prop['onClick'])

    def setText(self, text):
        self.widget.setText(text)

    def setStyleSheet(self, style):
        self.widget.setStyleSheet(style)

    def setAlignment(self, align):
        self.widget.setAlignment(align)

    def setEnabled(self, isEnabled):
        self.widget.setEnabled(isEnabled)

    def getWidget(self):
        return self.widget
