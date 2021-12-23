# -*- coding: utf-8 -*-

class Widget():
    def __init__(self, **kwargs):
        self.prop = kwargs
        self.widget = self.prop['widget']

        if "geometry" in kwargs:
            self.widget.setGeometry(self.prop['geometry'])
        if "text" in kwargs:
            self.widget.setText(self.prop['text'])
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

    def getWidget(self):
        return self.widget
