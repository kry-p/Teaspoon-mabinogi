import sqlite3

DB_PATH = './spoon.db'
RECIPE_MILESTONE = {
    'categoryName': ['[1] 저미기', '[2] 수비드', '[3] 발효',
                     '[4] 피자 만들기', '[5] 찌기', '[6] 파이 만들기',
                     '[7] 잼 만들기', '[8] 파스타 만들기', '[9] 볶기',
                     '[A] 튀기기', '[B] 면 만들기', '[C] 끓이기',
                     '[D] 반죽', '[E] 삶기', '[F] 굽기',
                     '[P] 혼합', '[N] 기타'],
    'categoryCode': ['1', '2', '3', '4',
                     '5', '6', '7', '8',
                     '9', 'A', 'B', 'C',
                     'D', 'E', 'F', 'P',
                     'N']
}


class DBManager:
    def __init__(self):
        self.data = sqlite3.connect(DB_PATH)
        self.cursor = self.data.cursor()

    # 사전에 지정된 카테고리 목록
    def getCategories(self):
        return RECIPE_MILESTONE

    # 요리 목록
    def getFoods(self, category):
        sql = "SELECT NAME FROM recipe WHERE RANK = '%s'" % category
        self.cursor.execute(sql)
        result = list(map(list, self.cursor.fetchall()))

        return result

    # 요리 정보 가져오기
    # ingredients: 재료1, 재료2, 재료3
    # specialEffects: 특수효과
    # stats:
    def getFoodInfo(self, food):
        result = {
            'ingredients': self.getFoodIngredients(food),
            'ratio': self.getFoodRatio(food),
            'specialEffects': self.getFoodSfx(food),
            'stats': self.getFoodStats(food)
        }
        return result

    # 재료 목록
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
        sql = 'SELECT SPECIALFX\
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
