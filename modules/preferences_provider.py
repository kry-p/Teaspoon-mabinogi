# -*- coding: utf-8 -*-
from PySide6.QtCore import QSettings, QStandardPaths, QFileSystemWatcher

defaultPreferences = {
    'color': ['#FFFF00', '#FF0000', '#FFFF00'],
    'initialWindowExpanded': True,
    'ratioDialogOpacity': 70,
    'ratioDialogDefaultPosition': {
        'x': 356,
        'y': 690
    },
    'ratioDialogSize': {
        'width': 243,
        'height': 10
    },
    'ratioBarColor': {
        0: '#ffff00',
        1: '#ff0000'
    },
    'favorites': {
        'item': []
    },
    'ratioBarLocked': False,
    'currentCategoryIndex': 0,
    'currentFood': '',
}

local_path = QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)
preferences = QSettings(local_path + "\\spoon.ini", QSettings.IniFormat)

# Settings watcher
paths = [local_path + '\\spoon.ini']
watcher = QFileSystemWatcher()
watcher.addPaths(paths)

def init():
    # 초기 설정 (설정값이 없을 때)
    for key, value in defaultPreferences.items():
        if not preferences.contains(key):
            preferences.setValue(key, value)


