# -*- coding: utf-8 -*-
'''
# Preferences provider for Spoon
# Made by kry-p
# https://github.com/kry-p/Teaspoon-mabinogi
'''
from PySide6.QtCore import QSettings, QStandardPaths, QFileSystemWatcher

# Default preferences
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
relative_path = '\\Yuzu\\Spoon\\settings.ini'
preferences = QSettings(local_path + relative_path, QSettings.IniFormat)

# Settings watcher
paths = [local_path + relative_path]
watcher = QFileSystemWatcher()
watcher.addPaths(paths)

# Initialize
def init():
    # Return default settings when QSettings doesn't have specific props
    for key, value in defaultPreferences.items():
        if not preferences.contains(key):
            preferences.setValue(key, value)

# Read from QSettings
def getPreferences(name):
    pref = preferences.value(name)

    if pref:
        return pref
    else:
        # If QSettings instance doesn't have specific props
        if defaultPreferences[name]:
            preferences.setValue(name, defaultPreferences[name])
            return defaultPreferences[name]
        return None


