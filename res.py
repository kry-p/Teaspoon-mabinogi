import os

import sys

if getattr(sys, 'frozen', False):
    root = sys._MEIPASS
else:
    root = os.path.dirname(__file__)
icon = os.path.join(root, 'cookie.ico')
icon_alt = os.path.join(root, 'cookie_alt.ico')

image_mini = os.path.join(root, 'mini.png')
image_full = os.path.join(root, 'full.png')
image_search = os.path.join(root, 'search.png')
image_tools = os.path.join(root, 'tools.png')
db_path = os.path.join(root, 'spoon.db')
