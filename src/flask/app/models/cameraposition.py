import psycopg2
from app.settings import DATABASE_CONFIG

class CameraPosition_m:
    
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            host=DATABASE_CONFIG["host"],
            database=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"])

    
    def list(self, cameraid):
        try:
            cur = self.conn.cursor()
            query = "select camerapositionid, positionnumber, positionname, cameraid from t_camera_position where cameraid='{}' order by positionnumber".format(cameraid)
            cur.execute(query)
            rows = cur.fetchall()
            if rows == None:
                return None, "Data not found"
            else:
                result = []
                for row in rows:
                    row = {
                        'camerapositionid': row[0],
                        'positionnumber': row[1],
                        'positionname': row[2],
                        'cameraid': row[3]
                    }
                    result.append(row)
                return result, ""
        except psycopg2.Error as e:
            return None, str(e)


    def readone(self, camerapositionid):
        try:
            cur = self.conn.cursor()
            query = "select camerapositionid, positionnumber, positionname, cameraid from t_camera_position where camerapositionid='{}' order by created".format(camerapositionid)
            cur.execute(query)
            row = cur.fetchone()
            if row == None:
                return None, "Data not found"
            else:
                result = {
                        'camerapositionid': row[0],
                        'positionnumber': row[1],
                        'positionname': row[2],
                        'cameraid': row[3]
                    }
                return result, ""
        except psycopg2.Error as e:
            return None, str(e)


    def getmax(self, cameraid):
        try:
            cur = self.conn.cursor()
            query = "select coalesce(max(positionnumber), 0) + 1 from t_camera_position where cameraid='{}'".format(cameraid)
            cur.execute(query)
            row = cur.fetchone()
            if row == None:
                return None, "Data not found"
            else:
                result = {
                        'max': row[0]
                    }
                return result, ""
        except psycopg2.Error as e:
            return None, str(e)


    def insert(self, positionname, cameraid, createby):
        try:
            max_value, message = self.getmax(cameraid)
            cur = self.conn.cursor()
            query = "insert into t_camera_position(camerapositionid, positionnumber, positionname, cameraid, createby) " \
                "values (default, {}, '{}', '{}', '{}')".format(max_value["max"], positionname, cameraid, createby)
            cur.execute(query)
            self.conn.commit()
            return True, max_value["max"], ""
        except psycopg2.Error as e:
            return False, -1, str(e)


    def update(self, camerapositionid, positionname):
        try:
            cur = self.conn.cursor()
            query = "update t_camera_position set positionname='{}' where camerapositionid='{}'".format(positionname, camerapositionid)
            cur.execute(query)
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)


    def delete(self, camerapositionid):
        try:
            cur = self.conn.cursor()
            query = "delete from t_camera_position where camerapositionid='{}'".format(camerapositionid)
            cur.execute(query)
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)