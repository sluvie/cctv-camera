import psycopg2
from app.settings import DATABASE_CONFIG

class Camera_m:
    
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            host=DATABASE_CONFIG["host"],
            database=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"])

    
    def list(self):
        try:
            cur = self.conn.cursor()
            query = "select cameraid, ip, webport, rtspport, username, password, dockerid, dockername, dockerport, onoff from t_camera order by created"
            cur.execute(query)
            rows = cur.fetchall()
            if rows == None:
                return None
            else:
                result = []
                for row in rows:
                    row = {
                        'cameraid': row[0],
                        'ip': row[1],
                        'webport': row[2],
                        'rtspport': row[3],
                        'username': row[4],
                        'password': row[5],
                        'dockerid': row[6],
                        'dockername': row[7],
                        'dockerport': row[8],
                        'onoff': row[9]
                    }
                    result.append(row)
                return result
        except psycopg2.Error as e:
            return None


    def readone(self, cameraid):
        try:
            cur = self.conn.cursor()
            query = "select cameraid, ip, webport, rtspport, username, password, dockerid, dockername, dockerport, onoff from t_camera where cameraid='{}' order by created".format(cameraid)
            cur.execute(query)
            row = cur.fetchone()
            if row == None:
                return None, "Data not found"
            else:
                result = {
                        'cameraid': row[0],
                        'ip': row[1],
                        'webport': row[2],
                        'rtspport': row[3],
                        'username': row[4],
                        'password': row[5],
                        'dockerid': row[6],
                        'dockername': row[7],
                        'dockerport': row[8],
                        'onoff': row[9]
                    }
                return result, ""
        except psycopg2.Error as e:
            return None, str(e)


    def insert(self, ip, port, rtspport, username, password, createby):
        try:
            cur = self.conn.cursor()
            query = "insert into t_camera(cameraid, ip, webport, rtspport, username, password, createby) values (default, '{}', '{}', '{}', '{}', '{}', '{}')".format(ip, port, rtspport, username, password, createby)
            cur.execute(query)
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)


    def update(self, cameraid, ip, port, rtspport, username, password, updateby):
        try:
            cur = self.conn.cursor()
            query = "update t_camera set ip='{}', webport='{}', rtspport='{}', username='{}', password='{}', updated=now(), updateby='{}' where cameraid='{}'".format(ip, port, rtspport, username, password, updateby, cameraid)
            cur.execute(query)
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)


    def delete(self, cameraid):
        try:
            cur = self.conn.cursor()
            query = "delete from t_camera where cameraid='{}'".format(cameraid)
            cur.execute(query)
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)


    def update_onoff(self, cameraid, onoff, updateby):
        try:
            cur = self.conn.cursor()
            query = "update t_camera set onoff={}, updated=now(), updateby='{}' where cameraid='{}'".format(onoff, updateby, cameraid)
            cur.execute(query)
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)