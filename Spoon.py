# -*- coding: utf-8 -*-
import sys
import os
import random
import res

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication,  Qt
from PySide6.QtGui import QIcon, QFont
from PySide6.QtUiTools import QUiLoader

from modules.fullwindow import FullWindow
from modules.preferences_provider import APP_VERSION, preferences

# from modules import window

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUi()

#     def initUi(self):
#         self.resize(QSize(190, 190))
#         self.center()
#         self.layout = QStackedLayout()

#         fullWindow = FullWindow()
#         miniWindow = MiniWindow()

#         self.layout.addWidget(fullWindow)
#         self.layout.addWidget(miniWindow)

#         self.layout.setCurrentIndex(0 if preferences.value('initialWindowExpanded') == 'true' else 1)
#         self.show()

#     def center(self):
#         qr = self.frameGeometry()
#         cp = QScreen().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())

if __name__ == "__main__":
    try:
        os.chdir(sys._MEIPASS)
    except:
        os.chdir(os.getcwd())
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    font = QFont('NanumGothic')
    font.setPointSize(9)
    if random.randrange(1, 31) == 7:
        app.setWindowIcon(QIcon(res.icon_alt))
    else:
        app.setWindowIcon(QIcon(res.icon))
    # if random.randrange(1, 11) == 7:
    #     app.setWindowIcon(QIcon(':/resources/cookie_alt.ico'))
    # else:
    #     app.setWindowIcon(QIcon(':/resources/cookie.ico'))
    app.setFont(QFont(font))

    # window = QStackedWidget()
    # window.setWindowTitle('Spoon')

    # # Change UI stack order
    # if preferences.value('initialWIndowExpanded') == 'false':
    #     window.addWidget(FullWindow())
    #     window.addWidget(MiniWindow())
    # else:
    #     window.addWidget(MiniWindow())
    #     window.addWidget(FullWindow())

    # window.show()

    # window = FullWindow() if preferences.value('initialWindowExpanded') == 'true' else MiniWindow()
    window = FullWindow(APP_VERSION)
    window.show()

    sys.exit(app.exec())


