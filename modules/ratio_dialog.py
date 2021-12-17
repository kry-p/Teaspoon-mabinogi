# -*- coding: utf-8 -*-
from PySide6.QtCore import (QRect, Qt)
from PySide6.QtGui import (QCursor, QFont)
from PySide6.QtWidgets import (QLabel, QMainWindow)
from .preferences_provider import preferences

rangeFont = QFont('Arial', 1)

# 비율 바 창
class RatioDialog(QMainWindow):
    def __init__(self, currentValue):
        super().__init__()
        self.m_flag = False
        self.currentWindowSize = {
            'width': preferences.value('ratioDialogSize')['width'],
            'height': preferences.value('ratioDialogSize')['height']
        }
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.move(preferences.value('ratioDialogDefaultPosition')['x'],
                  preferences.value('ratioDialogDefaultPosition')['y'])

        self.ratio = currentValue
        self.opacity = preferences.value('ratioDialogOpacity')

        if not self.opacity:
            preferences.setValue('ratioDialogOpacity', 70)

        self.initUI()

    # 새로운 값을 계산 후 반영
    def calculate(self):
        list = []
        sum = 0
        temp = 0
        color = preferences.value('ratioBarColor')
        for value in self.ratio:
            sum += value

        perValue = self.currentWindowSize['width'] / sum

        for ratioValue in self.ratio:
            if ratioValue == 0:
                continue
            list.append(perValue * ratioValue)

        for i in range(0, len(list)):
            self.labels[i].setGeometry(QRect(temp, 0, temp + list[i], 10))
            self.labels[i].setStyleSheet(
                'background-color: ' + color[i % 2] + ';')

            temp += list[i]

    # 저장된 값을 업데이트
    def update(self, newValue):
        self.ratio = newValue
        self.calculate()

    # UI 요소 초기화
    def initUI(self):
        self.setWindowOpacity(
            float((preferences.value('ratioDialogOpacity'))) * 0.01)
        self.resize(self.currentWindowSize['width'],
                    self.currentWindowSize['height'])
        self.setFixedSize(
            self.currentWindowSize['width'], self.currentWindowSize['height'])
        self.labels = [
            QLabel('', self),
            QLabel('', self),
            QLabel('', self),
        ]

        for i in range(0, 3):
            self.labels[i].setFont(rangeFont)

        self.calculate()
        self.show()

    # 마우스 클릭 이벤트
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and preferences.value('ratioBarLocked') == 'false':
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # Change mouse icon

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
