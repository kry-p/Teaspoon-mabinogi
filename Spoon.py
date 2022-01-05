# -*- coding: utf-8 -*-
import sys
import os
import random
import res

from PyQt5.QtWidgets import QApplication, QWidget, QStackedLayout
from PyQt5.QtCore import QCoreApplication, Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QScreen

from modules.fullwindow import FullWindow
from modules.miniwindow import MiniWindow
from modules.preferences_provider import APP_VERSION, getPreferences, preferences


if __name__ == "__main__":
    try:
        os.chdir(sys._MEIPASS)
    except:
        os.chdir(os.getcwd())
    # os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "1"
    
    # QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # QCoreApplication.setAttribute(Qt.AA_Use96Dpi, True)
    
    # QCoreApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
    
    # os.environ["QT_FONT_DPI"] = "96"
    

    app = QApplication([])
    
    font = QFont('NanumGothic')
    font.setPointSize(9)
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


