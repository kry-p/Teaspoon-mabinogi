# -*- coding: utf-8 -*-
'''
Excel sheet to SQLite DB converter script for Spoon
Made by kry-p
https://github.com/kry-p/Teaspoon-mabinogi
'''
import pandas as pd
import numpy as np
import sqlite3

DB_PATH = 'path here'
SHEET_PATH = 'path here'

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    data = pd.read_excel(SHEET_PATH)

    data.to_sql('recipe', conn, index = False)
    conn.close()
