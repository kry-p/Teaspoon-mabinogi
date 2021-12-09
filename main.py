# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QIcon

from ui.mainwindow import Ui_MainWindow


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    app.setWindowIcon(QIcon('resources/cookie.ico'))
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec())
