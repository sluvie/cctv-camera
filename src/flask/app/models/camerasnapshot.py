import psycopg2
from app.settings import DATABASE_CONFIG

class CameraSnapshot_m:
    
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            host=DATABASE_CONFIG["host"],
            database=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"])

    
    def list(self, cameraid):
        try:
            cur = self.conn.cursor()
            query = "select camerasnapshotid, camerabase64 from t_camera_snapshot where cameraid='{}' order by created".format(cameraid)
            cur.execute(query)
            rows = cur.fetchall()
            if rows == None:
                return None, "Data not found"
            else:
                result = []
                for row in rows:
                    row = {
                        'camerasnapshotid': row[0],
                        'camerabase64': row[1]
                    }
                    result.append(row)
                return result, ""
        except psycopg2.Error as e:
            return None, str(e)


    def readone(self, camerapositionid):
        try:
            cur = self.conn.cursor()
            query = "select camerasnapshotid, camerabase64 from t_camera_snapshot where where camerasnapshotid='{}' order by created".format(camerasnapshotid)
            cur.execute(query)
            row = cur.fetchone()
            if row == None:
                return None, "Data not found"
            else:
                result = {
                        'camerasnapshotid': row[0],
                        'camerabase64': row[1]
                    }
                return result, ""
        except psycopg2.Error as e:
            return None, str(e)


    def insert(self, camerabase64, cameraid, createby):
        try:
            cur = self.conn.cursor()
            query = "insert into t_camera_snapshot(camerasnapshotid, camerabase64, cameraid, createby) " \
                "values (default, decode(''{}'', 'base64'), '{}', '{}')".format(camerabase64, cameraid, createby)
            cur.execute(query)
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)


    def delete(self, camerasnapshotid):
        try:
            cur = self.conn.cursor()
            query = "delete from t_camera_snapshot where camerasnapshotid='{}'".format(camerasnapshotid)
            cur.execute(query)
            self.conn.commit()
            return True, ""
        except psycopg2.Error as e:
            return False, str(e)