# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QCoreApplication, Qt
from PySide6.QtUiTools import QUiLoader

from ui.dialogs import Ui_MainWindow


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec())
