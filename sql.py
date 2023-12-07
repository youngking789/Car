import pymysql


class Sql:
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='123456',
            database='aicarnumber',
            charset='utf8'
        )
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def insert(self, sql):
        sucess = self.cur.execute(sql)
        self.conn.commit()
        if sucess > 0:
            return True
        else:
            return False

    def delete(self, sql):
        sucess = self.cur.execute(sql)
        self.conn.commit()
        if sucess > 0:
            return True
        else:
            return False

    def select(self, sql):
        sucess = self.cur.execute(sql)
        if sucess > 0:
            return self.cur.fetchall()
        else:
            return 0

    def update(self, sql):
        sucess = self.cur.execute(sql)
        self.conn.commit()
        if sucess > 0:
            return True
        else:
            return False





