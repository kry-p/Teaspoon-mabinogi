# -*- coding: utf-8 -*-
'''
# Common elements and events for Spoon
# https://github.com/kry-p/Teaspoon-mabinogi
'''
from PyQt5.QtCore import (QEvent, pyqtSignal, QObject)

from .settings_dialog import SettingsDialog
from .ratio_dialog import RatioDialog

class Common():
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance   

    def __init__(self) -> None:
        self.settingsDialog = None
        self.ratioDialog = None

    def openSettingsDialog(self) -> None:
        if self.settingsDialog is None:
            self.settingsDialog = SettingsDialog()
        self.settingsDialog.show()

    def toggleRatioDialog(self, inputs : list) -> None:
        data = list(map(lambda value: 0 if value.text() ==
                        '' else int(value.text()), inputs))
        if self.ratioDialog is None and sum(data) != 0:
            self.ratioDialog = RatioDialog(data)
        else:
            if self.ratioDialog is not None:
                self.ratioDialog.close()
            self.ratioDialog = None

    def updateRatioDialog(self, inputs : list) -> None:
        if self.ratioDialog is not None:
            data = list(map(lambda value: 0 if value.text() ==
                        '' else int(value.text()), inputs))
            if sum(data) != 0:
                self.ratioDialog.update(data)

# Customized event
def customEvent(widget, event : QEvent):
    class Filter(QObject):
        signal = pyqtSignal()
        def eventFilter(self, obj, e) -> bool:
            if obj == widget and e.type() == event:
                self.signal.emit()
                return True
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.signal