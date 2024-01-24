import sqlite3

# 填写你的数据库用户名和密码
LIMIT = 4
DB = 'scores.db'

class User():
    def __init__(self):
        # 条件查询拼接sql语句
        self.major = ''
        self.year = ''
        self.semester = ''
        db = sqlite3.connect(DB)
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='score'")

        # 如果表不存在，那么创建它
        if cursor.fetchone() is None:
            cursor.execute("""
                CREATE Table score(
                    id TEXT PRIMARY KEY,          -- '选课课号'
                    year TEXT,                    -- '学年'
                    Semester TEXT,                -- '学期'
                    name TEXT,                    -- '课程名称'
                    credits REAL,                 -- '学分'
                    grade INTEGER,                -- '成绩'
                    gp REAL,                      -- '绩点'
                    regrade INTEGER,              -- '补考成绩'
                    major TEXT DEFAULT 'N'        -- '是否主修'
                );""")

        # 提交事务
        db.commit()
        db.close()
    
    # 查询表单总数
    def CountQuery(self):
        db = sqlite3.connect(DB)
        cursor = db.cursor()
        # table是sql语句
        sql = f'SELECT COUNT(*) FROM score WHERE 1 = 1 {self.year} {self.semester} {self.major}'
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result

    # 成绩信息查阅
    def Query(self,sql,*keys):
        db = sqlite3.connect(DB)
        cursor = db.cursor()
        cursor.execute(sql, keys)
        result = cursor.fetchall()
        db.close()
        return result

    # 增删改操纵(只能增)
    def Exec(self, sql,*values):
        db = sqlite3.connect(DB)
        cusor = db.cursor()
        try:
            cusor.execute(sql, values)
        except sqlite3.Error as e:
            print('error')
            print(e)
            db.rollback()
            return True
        finally:
            db.commit()
        db.close()

    # 查询成绩
    def ScoreQuery(self, page = 1):
        sql = f'SELECT id, name, credits, grade, gp, regrade FROM score WHERE 1 = 1 {self.year} {self.semester} {self.major} LIMIT {(page-1)*LIMIT}, {LIMIT}'
        res = self.Query(sql)
        return res
    
    # 增加成绩信息
    def AddScore(self,id,year,semester,name,credits,grade,gp,regrade=None,major='N'):
        sql = 'INSERT INTO score VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        return self.Exec(sql,id,year,semester,name,credits,grade,gp,regrade,major)
    
    # 爬虫查询
    def CrawlerQuery(self):
        sql = f'SELECT * FROM score WHERE 1 = 1 {self.year} {self.semester} {self.major}'
        res = self.Query(sql)
        return res
    
    # 当前学年的所有内容读取
    def YearAllQuery(self):
        sql = f'SELECT SUM(credits), SUM(gp*credits), ROUND(SUM(gp*credits)/SUM(credits),2), ROUND(SUM(grade*credits)/SUM(credits),2) FROM score WHERE 1=1 {self.year}'
        res = self.Query(sql)
        return res
    
    # 当前学年的主修内容读取
    def YearMajorQuery(self):
        sql = f'SELECT SUM(credits), SUM(gp*credits), ROUND(SUM(gp*credits)/SUM(credits),2), ROUND(SUM(grade*credits)/SUM(credits),2) FROM score WHERE major="Y" {self.year}'
        res = self.Query(sql)
        return res
    
    # 当前学期的所有内容读取
    def SemesterAllQuery(self):
        sql = f'SELECT SUM(credits), SUM(gp*credits), ROUND(SUM(gp*credits)/SUM(credits),2), ROUND(SUM(grade*credits)/SUM(credits),2) FROM score WHERE 1=1 {self.year} {self.semester}'
        res = self.Query(sql)
        return res
    
    # 当前学期的主修内容读取
    def SemesterMajorQuery(self):
        sql = f'SELECT SUM(credits), SUM(gp*credits), ROUND(SUM(gp*credits)/SUM(credits),2), ROUND(SUM(grade*credits)/SUM(credits),2) FROM score WHERE major="Y" {self.year} {self.semester}'
        res = self.Query(sql)
        return res