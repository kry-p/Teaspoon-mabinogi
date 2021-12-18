# encoding: utf-8
import sys
import res

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QIcon, QFontDatabase, QFont
from PySide6.QtUiTools import QUiLoader

from modules import window


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    font = QFont('NanumGothic')
    font.setPointSize(9)
    app.setWindowIcon(QIcon(':/resources/cookie.ico'))
    app.setFont(QFont(font))

    windowManager = window.manager
    windowManager.showMainWindow()
    
    sys.exit(app.exec())
