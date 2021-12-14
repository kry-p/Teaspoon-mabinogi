# encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QIcon, QFontDatabase, QFont
from PySide6.QtUiTools import QUiLoader

from ui.window import Ui_MainWindow
import res


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    font = QFont('NanumGothic')
    font.setPointSize(10)
    app.setWindowIcon(QIcon(':/resources/cookie.ico'))
    app.setFont(QFont(font))
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec())
