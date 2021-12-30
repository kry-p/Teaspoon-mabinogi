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
                        'MATK', 'DEF', 'PRT', 'MDEF', 'MPRT', 'SPECIALFX'],
    'npcList': ['케이틴', '글라니스', '고든', '프레이저', '셰나', '루카스', '제니퍼', '에피',
                '글라니테스', '반스트', '루와이', '피에릭', '글루아스', '카독', '아닉',
                '바날렌', '배리', '메이드', '교역', '렘 / 람', '마차']
}
RECIPE_MILESTONE['categoryName'].reverse()
RECIPE_MILESTONE['categoryColumns'].reverse()
RECIPE_MILESTONE['categoryCode'].reverse()

# Wrapper class
class DBManager:
    def __init__(self):
        self.data = sqlite3.connect(DB_PATH)
        self.cursor = self.data.cursor()

    # query
    def launchQuery(self, sql):
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
    def getCategories(self):
        return RECIPE_MILESTONE

    # Foods list
    def getFoods(self, category):
        sql = "SELECT NAME, ISEXT FROM recipe WHERE RANK = '%s'" % category
        return list(map(list, self.launchQuery(sql)))

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
        return self.launchQuery(sql)
        

    def getFoodRatio(self, food):
        sql = 'SELECT RATIO1, RATIO2, RATIO3\
               FROM recipe\
               WHERE NAME = \'%s\'' % food
        return self.launchQuery(sql)

    def getFoodSfx(self, food):
        sql = 'SELECT SPECIALFX, SFXDESC\
               FROM recipe\
               WHERE NAME = \'%s\'' % food
        return self.launchQuery(sql)

    def getFoodStats(self, food):
        sql = 'SELECT STR, INT, DEX, WIL, LUC,\
                      HP, MP, SP,\
                      MINDAM, MAXDAM,\
                      MATK, DEF, PRT, MDEF, MPRT\
               FROM recipe\
               WHERE NAME = \'%s\'' % food
        return self.launchQuery(sql)

    def getRelatedRecipe(self, food):
        sql = 'SELECT NAME\
               FROM recipe\
               WHERE NAME = \'' + food + '\''
        return self.launchQuery(sql)
    
    def getRelatedIngredient(self, food):
        sql = 'SELECT *\
               FROM ingredient\
               WHERE NAME = \'' + food + '\''
        return self.launchQuery(sql)

    def getRank(self, food):
        sql = 'SELECT RANK\
               FROM recipe\
               WHERE NAME = \'' + food + '\''
        response = self.launchQuery(sql)
        if len(response) == 0:
            return -1
        else:
            return response[0][0]

    ''' ---------- Search ---------- '''
    def searchByIngredient(self, ingredient):
        sql = 'SELECT NAME, ISEXT\
               FROM recipe\
               WHERE INGREDIENT1 LIKE \'%' + ingredient + '%\'\
                  OR INGREDIENT2 LIKE \'%' + ingredient + '%\'\
                  OR INGREDIENT3 LIKE \'%' + ingredient + '%\''
        return self.launchQuery(sql)

    def searchByName(self, name):
        sql = 'SELECT NAME, ISEXT\
               FROM recipe\
               WHERE NAME LIKE \'%' + name + '%\''
        return self.launchQuery(sql)
    
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

        sql = 'SELECT NAME, ISEXT\
               FROM recipe\
               WHERE %s' % constraiants
        return self.launchQuery(sql)