import psycopg2
from app.settings import DATABASE_CONFIG

class Camera_m:
    
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            host=DATABASE_CONFIG["host"],
            port=DATABASE_CONFIG["port"],
            database=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"])

    
    def list(self):
        try:
            cur = self.conn.cursor()
            query = "select cameraid, ip, webport, rtspport, username, password, dockerid, dockername, dockerport, onoff, companyname, placename, positionorder from t_camera order by positionorder"
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
                        'onoff': row[9],
                        'companyname': row[10],
                        'placename': row[11],
                        'positionorder': row[12]
                    }
                    result.append(row)
                return result
        except psycopg2.Error as e:
            return None


    def readone(self, cameraid):
        try:
            cur = self.conn.cursor()
            query = "select cameraid, ip, webport, rtspport, username, password, dockerid, dockername, dockerport, onoff, companyname, placename, positionorder from t_camera where cameraid=%s order by created"
            cur.execute(query, (cameraid, ))
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
                        'onoff': row[9],
                        'companyname': row[10],
                        'placename': row[11],
                        'positionorder': row[12]
                    }
                return result, ""
        except psycopg2.Error as e:
            return None, str(e)


    def insert(self, companyname, placename, positionorder, ip, port, rtspport, username, password, createby):
        try:
            cur = self.conn.cursor()
            query = "insert into t_camera(cameraid, companyname, placename, positionorder, ip, webport, rtspport, username, password, createby) " \
                "values (default, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(query, (companyname, placename, positionorder, ip, port, rtspport, username, password, createby, ))
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)


    def update(self, cameraid, companyname, placename, positionorder, ip, port, rtspport, username, password, updateby):
        try:
            cur = self.conn.cursor()
            query = "update t_camera set companyname=%s, placename=%s, positionorder=%s, " \
                "ip=%s, webport=%s, rtspport=%s, username=%s, password=%s, updated=now(), updateby=%s where cameraid=%s"
            cur.execute(query, (companyname, placename, positionorder, ip, port, rtspport, username, password, updateby, cameraid, ))
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)


    def delete(self, cameraid):
        try:
            cur = self.conn.cursor()
            query = "delete from t_camera where cameraid=%s"
            cur.execute(query, (cameraid, ))
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)


    def update_onoff(self, cameraid, onoff, updateby):
        try:
            cur = self.conn.cursor()
            query = "update t_camera set onoff=%s, updated=now(), updateby=%s where cameraid=%s"
            cur.execute(query, (onoff, updateby, cameraid))
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)