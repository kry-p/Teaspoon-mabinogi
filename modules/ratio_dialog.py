# -*- coding: utf-8 -*-
'''
# Food ratio dialog for Spoon
# https://github.com/kry-p/Teaspoon-mabinogi
'''
from PySide6.QtCore import (QRect, Qt)
from PySide6.QtGui import (QCursor, QFont)
from PySide6.QtWidgets import (QLabel, QMainWindow)
from .preferences_provider import getPreferences, watcher

rangeFont = QFont('Arial', 1)

# Ratio bar window
class RatioDialog(QMainWindow):
    def __init__(self, currentValue):
        super().__init__()
        self.setWindowTitle('비율')
        self.m_flag = False
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.ratio = currentValue

        self.opacity = getPreferences('ratioDialogOpacity')
        self.move(getPreferences('ratioDialogDefaultPosition')['x'],
                  getPreferences('ratioDialogDefaultPosition')['y'])
        self.initUI()

    # Calculate new ratio and display
    def draw(self):
        list = []
        sum = 0
        temp = 0
        
        # Get preferences
        color = getPreferences('ratioBarColor')
        self.opacity = getPreferences('ratioDialogOpacity')
        self.currentWindowSize = {
            'width': getPreferences('ratioDialogSize')['width'],
            'height': getPreferences('ratioDialogSize')['height']
        }
        self.setWindowOpacity(
            float((getPreferences('ratioDialogOpacity'))) * 0.01)
        self.resize(self.currentWindowSize['width'],
                    self.currentWindowSize['height'])
        self.setFixedSize(
            self.currentWindowSize['width'], self.currentWindowSize['height'])

        for value in self.ratio:
            sum += value

        perValue = self.currentWindowSize['width'] / sum

        for ratioValue in self.ratio:
            if ratioValue == 0:
                continue
            list.append(perValue * ratioValue)

        for i in range(0, len(list)):
            self.labels[i].setGeometry(QRect(temp, 0, temp + list[i], self.currentWindowSize['height']))
            self.labels[i].setStyleSheet(
                'background-color: ' + color[i % 2] + ';')

            temp += list[i]
        
        for i in range(len(list), 3):
            self.labels[i].setStyleSheet(
                'background-color: rgba(255, 255, 255, 0);')

    # Set new ratio value
    def update(self, newValue):
        self.ratio = newValue
        self.draw()

    # Initialize UI elements
    def initUI(self):
        self.labels = [
            QLabel('', self),
            QLabel('', self),
            QLabel('', self),
        ]
        for label in self.labels:
            label.setFont(rangeFont)
        self.draw()
        self.show()

    # Mouse event
    def mousePressEvent(self, event):
        ratioBarLocked = getPreferences('ratioBarLocked')
        if event.button() == Qt.LeftButton and (ratioBarLocked == 'false' or ratioBarLocked == False):
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
