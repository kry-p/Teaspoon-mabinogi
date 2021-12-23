# -*- coding: utf-8 -*-
'''
# Food ratio dialog for Spoon
# Made by kry-p
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
        self.m_flag = False
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.ratio = currentValue

        self.opacity = getPreferences('ratioDialogOpacity')
        self.initUI()

    # Calculate new ratio and display
    def draw(self):
        list = []
        sum = 0
        temp = 0
        
        # Get preferences
        color = getPreferences('ratioBarColor')
        self.opacity = getPreferences('ratioDialogOpacity')
        self.move(getPreferences('ratioDialogDefaultPosition')['x'],
                  getPreferences('ratioDialogDefaultPosition')['y'])
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
        watcher.fileChanged.connect(self.draw)
        self.draw()
        self.show()

    # Mouse event
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and getPreferences('ratioBarLocked') != 'true':
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
