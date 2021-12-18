from .preferences_provider import preferences
from .fullwindow import FullWindow
from .miniwindow import MiniWindow

class WindowManager():
    def __init__(self):
        self.miniApp = None
        self.fullApp = None

    def showMainWindow(self):
        if preferences.value('initialWindowExpanded') == 'true':
            self.fullApp = FullWindow()
            self.fullApp.show()
        else:
            self.miniApp = MiniWindow()
            self.miniApp.show()

    def onChangeWindow(self, window):
        pass

manager = WindowManager()
