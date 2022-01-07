# -*- coding: utf-8 -*-
'''
# Preferences provider for Spoon
# https://github.com/kry-p/Teaspoon-mabinogi
'''
import os
from PyQt5.QtCore import QSettings, QStandardPaths, QFileSystemWatcher
from pathlib import Path

# Version
APP_VERSION = 'v0.2 beta 5'
BUILD_NUMBER = 11

# Default preferences
defaultPreferences = {
    'buildNumber': BUILD_NUMBER,
    'color': ['#FFFF00', '#FF0000', '#FFFF00'],
    'initialWindowExpanded': True,
    'ratioDialogOpacity': 70,
    'ratioDialogPosition': {
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
    'currentTabIndex': 0,
    'currentCategoryIndex': 0,
    'currentCategoryItemIndex': -1,
    'currentFavoritesIndex': -1,
    'currentFood': '',
}

local_path = QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)
relative_path = '\\Yuzu\\Spoon\\'
filename = 'settings.ini'

# Initialize
def init():
    # if preferences based on previous build
    if not preferences.contains('buildNumber') or int(getPreferences('buildNumber')) < BUILD_NUMBER:
        resetIncompatibles()

    # Return default settings when QSettings doesn't have specific props
    for key, value in defaultPreferences.items():
        if not preferences.contains(key):
            preferences.setValue(key, value)

def makeDir(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

# Reset incompatible preferences
def resetIncompatibles():
    reset = ['buildNumber', 'currentFood', 'currentTabIndex', 
             'currentCategoryIndex', 'currentCategoryItemIndex', 'currentFavoritesIndex']

    for key in reset:
        preferences.setValue(key, defaultPreferences[key])
    
# Read from QSettings
def getPreferences(name):
    pref = preferences.value(name)

    if pref:
        return pref
    else:
        # If QSettings instance doesn't have specific props
        return defaultPreferences[name]

# Create preferences file
makeDir(local_path + relative_path)
file = Path(local_path + relative_path + filename)
file.touch(exist_ok = True)

preferences = QSettings(local_path + relative_path + filename, QSettings.IniFormat)

# Settings watcher
paths = [local_path + relative_path + filename]
watcher = QFileSystemWatcher()
watcher.addPaths(paths)
