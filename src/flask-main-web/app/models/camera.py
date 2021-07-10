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
            query = "select cameraid, ip, webport, rtspport, username, password, dockerid, dockername, dockerport from t_camera"
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
                    }
                    result.append(row)
                return result
        except psycopg2.Error as e:
            return None


    def insert(self, ip, port, rtspport, username, password, createby):
        try:
            cur = self.conn.cursor()
            query = "insert into t_camera values (default, '{}', '{}', '{}', '{}', '{}', '', '', '', now(), '{}', null, null)".format(ip, port, rtspport, username, password, createby)
            cur.execute(query)
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)