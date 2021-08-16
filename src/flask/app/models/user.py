import psycopg2
import psycopg2.extras
from app.settings import DATABASE_CONFIG

class User_m:
    
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            host=DATABASE_CONFIG["host"],
            port=DATABASE_CONFIG["port"],
            database=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"])

        psycopg2.extras.register_uuid()

    
    def list(self, deleteflag=0):
        try:
            cur = self.conn.cursor()
            query = "select userid, username, password, name, isadmin from t_user where deleteflag=%s order by created"
            cur.execute(query, (deleteflag, ))
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


    def readone(self, userid):
        try:
            cur = self.conn.cursor()
            query = "select userid, username, password, name, isadmin from t_user where userid=%s"
            cur.execute(query, (userid, ))
            row = cur.fetchone()
            if row == None:
                return None, "Data not found"
            else:
                result = {
                        'userid': row[0],
                        'username': row[1],
                        'password': row[2],
                        'name': row[3],
                        'isadmin': row[4]
                    }
                return result, ""
        except psycopg2.Error as e:
            return None, str(e)

    
    def get(self, username, deleteflag=0):
        try:
            cur = self.conn.cursor()
            query = "select userid, username, password, name, isadmin from t_user where username=%s and deleteflag=%s"
            cur.execute(query, (username, deleteflag, ))
            row = cur.fetchone()
            if row == None:
                return None
            else:
                result = {
                        'userid': row[0],
                        'username': row[1],
                        'password': row[2],
                        'name': row[3],
                        'isadmin': row[4]
                    }
                return result
        except psycopg2.Error as e:
            return None

    def get_fromsession(self, sessionid):
        try:
            cur = self.conn.cursor()
            query = "select t.userid, t.username, t.password, t.name, t.isadmin from t_user t join t_user_session us on t.userid=us.userid where us.sessionid=%s limit 1"
            cur.execute(query, (sessionid, ))
            row = cur.fetchone()
            if row == None:
                return None
            else:
                result = {
                        'userid': row[0],
                        'username': row[1],
                        'password': row[2],
                        'name': row[3],
                        'isadmin': row[4]
                    }
                return result
        except psycopg2.Error as e:
            print(e)
            return None

    def get_sessionid(self, username):
        try:
            cur = self.conn.cursor()
            query = "select sessionid from t_user_session where username=%s order by created desc limit 1"
            cur.execute(query, (username, ))
            row = cur.fetchone()
            if row == None:
                return None
            else:
                result = row[0]
                return result
        except psycopg2.Error as e:
            return None


    def insert(self, username, password, name, isadmin, createby):
        try:
            cur = self.conn.cursor()
            query = "insert into t_user(userid, username, password, name, isadmin, createby) values (default, %s, %s, %s, %s, %s)"
            cur.execute(query, (username, password, name, isadmin, createby, ))
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)


    def update(self, userid, password, name, isadmin, updateby):
        try:
            cur = self.conn.cursor()
            query = "update t_user set password=%s, name=%s, isadmin=%s, updated=now(), updateby=%s where userid=%s"
            cur.execute(query, (password, name, isadmin, updateby, userid, ))
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)


    def delete(self, userid, updateby):
        try:
            cur = self.conn.cursor()
            query = "update t_user set deleteflag=1, updated=now(), updateby=%s where userid=%s"
            cur.execute(query, (updateby, userid, ))
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)

    def create_session(self, userid, username):
        try:
            cur = self.conn.cursor()
            query = "insert into t_user_session(sessionid, userid, username, createby) values (default, %s, %s, %s)"
            cur.execute(query, (userid, username, username, ))
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)