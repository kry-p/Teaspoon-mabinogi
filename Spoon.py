# -*- coding: utf-8 -*-
import sys
import os
import random
import res

from PyQt5.QtWidgets import (QApplication)
from PyQt5.QtCore import (QCoreApplication, Qt)
from PyQt5.QtGui import (QIcon, QFont)

from modules.fullwindow import FullWindow
from modules.miniwindow import MiniWindow
from modules.preferences_provider import APP_VERSION, getPreferences, initPreferences


if __name__ == "__main__":
    try:
        os.chdir(sys._MEIPASS)
    except:
        os.chdir(os.getcwd())
    initPreferences()
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication([])
    font = QFont('NanumGothic')
    font.setPointSize(9)

    # Randomized app icon
    if random.randrange(1, 31) == 7:
        app.setWindowIcon(QIcon(res.icon_alt))
    else:
        app.setWindowIcon(QIcon(res.icon))
    
    app.setFont(QFont(font))

    global mini
    global full

    mini = MiniWindow(APP_VERSION)
    full = FullWindow(APP_VERSION)

    mini.setFullWindow(full)
    full.setMiniWindow(mini)
    
    if getPreferences('initialWindowExpanded') == 'false':
        window = mini
    else:
        window = full
    window.show()
    sys.exit(app.exec())


