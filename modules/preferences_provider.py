from PySide6.QtCore import QSettings

defaultPreferences = {
    'color': ['#FFFF00', '#FF0000', '#FFFF00'],
    'initialWindowExpanded': True,
    'ratioDialogOpacity': 70,
    'ratioDialogDefaultPosition': {
        'x': 356,
        'y': 690
    },
    'ratioDialogSize': {
        'width': 243,
        'height': 10
    },
    'ratioBarColor': {
        0: '#ffff00',
        1: '#ff0000'
    },
    'favorites': [],
    'ratioBarLocked': False,
    'currentCategoryIndex': 0,
    'currentFood': ''
}
preferences = QSettings('Yuzu', 'Spoon')
