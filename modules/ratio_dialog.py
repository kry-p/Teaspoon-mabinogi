# -*- coding: utf-8 -*-
'''
# Food ratio dialog for Spoon
# https://github.com/kry-p/Teaspoon-mabinogi
'''
from PyQt5.QtCore import (QEvent, QRect, Qt)
from PyQt5.QtGui import (QCursor, QFont)
from PyQt5.QtWidgets import (QLabel, QMainWindow)
from .preferences_provider import (getPreferences, preferences)

RANGE_FONT = QFont('Arial', 1)

# Ratio bar window
class RatioDialog(QMainWindow):
    def __init__(self, currentValue : list) -> None:
        super().__init__()
        self.setWindowTitle('비율')
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.mouseFlag : bool = False
        self.ratio = currentValue

        self.opacity = getPreferences('ratioDialogOpacity')
        self.initUI()

    # Initialize UI elements
    def initUI(self) -> None:
        self.labels = [QLabel('', self), QLabel('', self), QLabel('', self)]
        for label in self.labels:
            label.setFont(RANGE_FONT)
        self.draw()
        self.show()

    # Calculate new ratio and display
    def draw(self) -> None:
        list = []
        sum : int = 0
        temp : int = 0
        
        # Get preferences
        color = getPreferences('ratioBarColor')
        self.opacity = getPreferences('ratioDialogOpacity')
        self.currentWindowSize = {
            'width': getPreferences('ratioDialogSize')['width'],
            'height': getPreferences('ratioDialogSize')['height']
        }
        self.move(getPreferences('ratioDialogPosition')['x'],
                  getPreferences('ratioDialogPosition')['y'])
        self.setWindowOpacity(
            float(int(getPreferences('ratioDialogOpacity')) - 1) * 0.01)
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
            self.labels[i].setGeometry(QRect(int(temp), 0, int(temp + list[i]), self.currentWindowSize['height']))
            self.labels[i].setStyleSheet('background-color: \'%s\';' % color[i % 2])
            temp += list[i]
        
        for i in range(len(list), 3):
            self.labels[i].setStyleSheet('background-color: rgba(255, 255, 255, 0);')

    # Set new ratio value
    def update(self, newValue : list) -> None:
        self.ratio = newValue
        self.draw()

    # Mouse event
    def mousePressEvent(self, event : QEvent) -> None:
        ratioBarLocked = getPreferences('ratioBarLocked')
        if event.button() == Qt.LeftButton and (ratioBarLocked == 'false' or ratioBarLocked == False):
            self.mouseFlag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event : QEvent) -> None:
        if Qt.LeftButton and self.mouseFlag:
            self.move(event.globalPos() - self.m_Position)
            
            geometry = self.geometry()
            val = {
                'x': geometry.x(),
                'y': geometry.y()
            }
            preferences.setValue('ratioDialogPosition', val)
            event.accept()

    def mouseReleaseEvent(self, event : QEvent) -> None:
        self.mouseFlag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
