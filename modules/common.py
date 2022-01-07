# -*- coding: utf-8 -*-
'''
# Main window for Spoon
# https://github.com/kry-p/Teaspoon-mabinogi
'''
from PyQt5.QtCore import pyqtSignal, QObject

from .settings_dialog import SettingsDialog
from .ratio_dialog import RatioDialog

from .settings_dialog import preferences

class Common():
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance   

    def __init__(self):
        self.settingsDialog = None
        self.ratioDialog = None

    def openSettingsDialog(self):
        if self.settingsDialog is None:
            self.settingsDialog = SettingsDialog()
        self.settingsDialog.show()

    def toggleRatioDialog(self, inputs):
        data = list(map(lambda value: 0 if value.text() ==
                        '' else int(value.text()), inputs))
        test = sum(data)
        if self.ratioDialog is None and test != 0:
            self.ratioDialog = RatioDialog(data)
        else:
            if self.ratioDialog is not None:
                self.ratioDialog.close()
            self.ratioDialog = None

# Customized event
def customEvent(widget, event):
    class Filter(QObject):
        signal = pyqtSignal()
        def eventFilter(self, obj, e):
            if obj == widget and e.type() == event:
                self.signal.emit()
                return True
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.signal