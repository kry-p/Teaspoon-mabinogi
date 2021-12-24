# -*- coding: utf-8 -*-
'''
Database wrapper class for Spoon
using SQLite
'''
import sqlite3

DB_PATH = './spoon.db'
RECIPE_MILESTONE = {
    'categoryName': ['[1] 저미기', '[2] 수비드', '[3] 발효',
                     '[4] 피자 만들기', '[5] 찌기', '[6] 파이 만들기',
                     '[7] 잼 만들기', '[8] 파스타 만들기', '[9] 볶기',
                     '[A] 튀기기', '[B] 면 만들기', '[C] 끓이기',
                     '[D] 반죽', '[E] 삶기', '[F] 굽기',
                     '[P] 혼합'],
    'categoryCode': ['1', '2', '3', '4',
                     '5', '6', '7', '8',
                     '9', 'A', 'B', 'C',
                     'D', 'E', 'F', 'P'],
    'categoryColumns': ['STR', 'INT', 'DEX', 'WIL', 'LUC',
                        'HP', 'MP', 'SP',
                        'MINDAM', 'MAXDAM',
                        'MATK', 'DEF', 'PRT', 'MDEF', 'MPRT', 'SPECIALFX']
}
RECIPE_MILESTONE['categoryName'].reverse()
RECIPE_MILESTONE['categoryColumns'].reverse()
RECIPE_MILESTONE['categoryCode'].reverse()

# Wrapper class
class DBManager:
    def __init__(self):
        self.data = sqlite3.connect(DB_PATH)
        self.cursor = self.data.cursor()

    # Pre-specified categories
    def getCategories(self):
        return RECIPE_MILESTONE

    # Foods list
    def getFoods(self, category):
        sql = "SELECT NAME FROM recipe WHERE RANK = '%s'" % category
        self.cursor.execute(sql)
        result = list(map(list, self.cursor.fetchall()))

        return result

    # Get list of foods
    # ingredients: 재료 1, 재료 2, 재료 3
    # specialEffects: 
    # stats: 스테이터스 효과
    def getFoodInfo(self, food):
        result = {
            'ingredients': self.getFoodIngredients(food),
            'ratio': self.getFoodRatio(food),
            'specialEffects': self.getFoodSfx(food),
            'stats': self.getFoodStats(food)
        }
        return result

    def getFoodIngredients(self, food):
        sql = 'SELECT INGREDIENT1, INGREDIENT2, INGREDIENT3\
               FROM recipe\
               WHERE NAME = \'%s\'' % food
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getFoodRatio(self, food):
        sql = 'SELECT RATIO1, RATIO2, RATIO3\
               FROM recipe\
               WHERE NAME = \'%s\'' % food
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getFoodSfx(self, food):
        sql = 'SELECT SPECIALFX, SFXDESC\
               FROM recipe\
               WHERE NAME = \'%s\'' % food
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getFoodStats(self, food):
        sql = 'SELECT STR, INT, DEX, WIL, LUC,\
                      HP, MP, SP,\
                      MINDAM, MAXDAM,\
                      MATK, DEF, PRT, MDEF, MPRT\
               FROM recipe\
               WHERE NAME = \'%s\'' % food
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def searchByIngredient(self, ingredient):
        sql = 'SELECT NAME\
               FROM recipe\
               WHERE INGREDIENT1 LIKE \'%' + ingredient + '%\'\
                  OR INGREDIENT2 LIKE \'%' + ingredient + '%\'\
                  OR INGREDIENT3 LIKE \'%' + ingredient + '%\''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def searchByName(self, name):
        sql = 'SELECT NAME\
               FROM recipe\
               WHERE NAME LIKE \'%' + name + '%\''
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def searchByEffect(self, selected):
        # OR operation
        constraiants = ''
        for i in range(len(selected)):
            if selected[i]:
                if constraiants == '':
                    constraiants += "%s NOT NULL " % RECIPE_MILESTONE['categoryColumns'][15 - i]
                elif i == (len(selected) - 1):
                    constraiants += 'OR %s NOT NULL' % RECIPE_MILESTONE['categoryColumns'][15 - i]
                else:
                    constraiants += 'OR %s NOT NULL ' % RECIPE_MILESTONE['categoryColumns'][15 - i]

        sql = 'SELECT NAME\
               FROM recipe\
               WHERE %s' % constraiants
        self.cursor.execute(sql)
        return self.cursor.fetchall()

        
