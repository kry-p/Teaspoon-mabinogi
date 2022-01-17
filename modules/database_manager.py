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
    'effectColumns': ['STR', 'INT', 'DEX', 'WIL', 'LUC',
                        'HP', 'MP', 'SP',
                        'MINDAM', 'MAXDAM',
                        'MATK', 'DEF', 'PRT', 'MDEF', 'MPRT', 'SPECIALFX'],
    'npcList': ['식료품점', '글라니스', '고든', '프레이저', '셰나', '루카스', '글루아스',
                '반스트', '아닉', '카독', '바날렌', '배리', '메이드', '윌리엄', '렘 / 람',
                '마차', '채집', '드랍', '퀘스트', '제작']
}
RECIPE_MILESTONE['categoryName'].reverse()
RECIPE_MILESTONE['effectColumns'].reverse()
RECIPE_MILESTONE['categoryCode'].reverse()

# Wrapper class
class DBManager:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance   

    def __init__(self) -> None:
        self.data = sqlite3.connect(DB_PATH)
        self.cursor = self.data.cursor()

    # query
    def launchQuery(self, sql : str):
        try:
            self.cursor.execute(sql)
            response =  {
                'success': True,
                'result': self.cursor.fetchall()
            }
        except sqlite3.Error as e:
            response = {
                'success': False,
                'result': e
            }
        finally:
            if response['success'] is True:
                return response['result']
            else:
                return []

    ''' ---------- SELECT ---------- '''
    # Pre-specified categories
    def getCategories(self) -> list:
        return RECIPE_MILESTONE

    # Foods list
    def getFoods(self, category : str) -> list:
        sql = "SELECT NAME, ISEXT FROM recipe WHERE RANK = '%s'" % category
        return list(map(list, self.launchQuery(sql)))

    # Get list of foods
    # ingredients: 재료 1, 재료 2, 재료 3
    # specialEffects: 
    # stats: 스테이터스 효과
    def getFoodInfo(self, food : str) -> dict:
        result = {
            'ingredients': self.getFoodIngredients(food),
            'ratio': self.getFoodRatio(food),
            'specialEffects': self.getFoodSfx(food),
            'stats': self.getFoodStats(food)
        }
        return result

    def getFoodIngredients(self, food : str):
        sql = 'SELECT INGREDIENT1, INGREDIENT2, INGREDIENT3\
               FROM recipe\
               WHERE NAME = \'%s\'' % food
        return self.launchQuery(sql)
        
    def getFoodRatio(self, food : str):
        sql = 'SELECT RATIO1, RATIO2, RATIO3\
               FROM recipe\
               WHERE NAME = \'%s\'' % food
        return self.launchQuery(sql)

    def getFoodSfx(self, food : str):
        sql = 'SELECT SPECIALFX1, SPECIALFX2, SFXDESC1, SFXDESC2\
               FROM recipe\
               WHERE NAME = \'%s\'' % food
        return self.launchQuery(sql)

    def getFoodStats(self, food : str):
        sql = 'SELECT STR, INT, DEX, WIL, LUC,\
                      HP, MP, SP,\
                      MINDAM, MAXDAM,\
                      MATK, DEF, PRT, MDEF, MPRT\
               FROM recipe\
               WHERE NAME = \'%s\'' % food
        return self.launchQuery(sql)

    def getRelatedRecipe(self, food : str):
        sql = 'SELECT NAME\
               FROM recipe\
               WHERE NAME = \'' + food + '\''
        return self.launchQuery(sql)
    
    def getRelatedIngredient(self, food : str):
        sql = 'SELECT *\
               FROM ingredient\
               WHERE NAME = \'' + food + '\''
        return self.launchQuery(sql)

    def getRank(self, food : str):
        sql = 'SELECT RANK\
               FROM recipe\
               WHERE NAME = \'' + food + '\''
        response = self.launchQuery(sql)
        if len(response) == 0:
            return -1
        else:
            return response[0][0]

    def getExt(self, food : str):
        sql = 'SELECT ISEXT\
               FROM recipe\
               WHERE NAME = \'' + food + '\''
        response = self.launchQuery(sql)
        return self.launchQuery(sql)

    ''' ---------- Search ---------- '''
    def searchByIngredient(self, ingredient : str):
        sql = 'SELECT NAME, ISEXT\
               FROM recipe\
               WHERE INGREDIENT1 LIKE \'%' + ingredient + '%\'\
                  OR INGREDIENT2 LIKE \'%' + ingredient + '%\'\
                  OR INGREDIENT3 LIKE \'%' + ingredient + '%\''
        return self.launchQuery(sql)

    def searchByName(self, name : str):
        sql = 'SELECT NAME, ISEXT\
               FROM recipe\
               WHERE NAME LIKE \'%' + name + '%\''
        return self.launchQuery(sql)
    
    def searchByEffect(self, query : dict):
        constraiants = ''
        logic = query['logic']
        del(query['logic'])
        idx : int = 0
        
        for key, value in query.items():
            if key == 'SPECIALFX':
                if idx < len(query) - 1:
                    constraiants += ' %s NOT NULL' % key + ' %s' % logic[idx]
                else:
                    constraiants += ' %s NOT NULL' % key
            elif len(value) == 0:
                if idx < len(query) - 1:
                    constraiants += ' %s != 0' % key + ' %s' % logic[idx]
                else:
                    constraiants += ' %s != 0' % key
            else:
                if idx < len(query) - 1:
                    constraiants += ' %s BETWEEN ' % key + value[0] + ' AND ' + value[1] + ' %s' % logic[idx]
                else:
                    constraiants +=' %s BETWEEN ' % key + value[0] + ' AND ' + value[1]
            idx += 1
            
        sql = 'SELECT NAME, ISEXT\
               FROM recipe\
               WHERE %s' % constraiants
        return self.launchQuery(sql)
