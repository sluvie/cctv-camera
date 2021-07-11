import psycopg2
from app.settings import DATABASE_CONFIG

class User_m:
    
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            host=DATABASE_CONFIG["host"],
            database=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"])

    
    def list(self, deleteflag=0):
        try:
            cur = self.conn.cursor()
            query = "select userid, username, password, name, isadmin from t_user where deleteflag={} order by created".format(deleteflag)
            cur.execute(query)
            rows = cur.fetchall()
            if rows == None:
                return None
            else:
                result = []
                for row in rows:
                    row = {
                        'userid': row[0],
                        'username': row[1],
                        'password': row[2],
                        'name': row[3],
                        'isadmin': row[4]
                    }
                    result.append(row)
                return result
        except psycopg2.Error as e:
            return None


    def insert(self, username, password, name, isadmin, createby):
        try:
            cur = self.conn.cursor()
            query = "insert into t_user(userid, username, password, name, isadmin, createby) values (default, '{}', '{}', '{}', {}, '{}')".format(username, password, name, isadmin, createby)
            cur.execute(query)
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)


    def update(self, userid, password, name, isadmin, updateby):
        try:
            cur = self.conn.cursor()
            query = "update t_user set password='{}', name='{}', isadmin={}, updated=now(), updateby='{}' where userid='{}'".format(password, name, isadmin, updateby, userid)
            cur.execute(query)
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)


    def delete(self, userid, updateby):
        try:
            cur = self.conn.cursor()
            query = "update t_user set deleteflag=1, updated=now(), updateby='{}' where userid='{}'".format(updateby, userid)
            cur.execute(query)
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)