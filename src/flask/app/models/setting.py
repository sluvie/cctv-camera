import psycopg2
import psycopg2.extras
from app.settings import DATABASE_CONFIG

class Setting_m:
    
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            host=DATABASE_CONFIG["host"],
            port=DATABASE_CONFIG["port"],
            database=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"])

        psycopg2.extras.register_uuid()


    def list_keytag(self, keytag1, keytag2):
        try:
            cur = self.conn.cursor()
            query = "select settingid, tag1, tag2, tag3, tag4, tag5 from t_setting where keytag1=%s and keytag2=%s"
            cur.execute(query, (keytag1, keytag2, ))
            rows = cur.fetchall()
            if rows == None:
                return None
            else:
                result = []
                for row in rows:
                    row = {
                        'settingid': row[0],
                        'tag1': row[1],
                        'tag2': row[2],
                        'tag3': row[3],
                        'tag4': row[4],
                        'tag5': row[5]
                    }
                    result.append(row)
                return result
        except psycopg2.Error as e:
            return None
            

    def readone_keytag(self, keytag1, keytag2):
        try:
            cur = self.conn.cursor()
            query = "select settingid, tag1, tag2, tag3, tag4, tag5 from t_setting where keytag1=%s and keytag2=%s"
            cur.execute(query, (keytag1, keytag2, ))
            row = cur.fetchone()
            if row == None:
                return None, "Data not found"
            else:
                result = {
                        'settingid': row[0],
                        'tag1': row[1],
                        'tag2': row[2],
                        'tag3': row[3],
                        'tag4': row[4],
                        'tag5': row[5]
                    }
                return result, ""
        except psycopg2.Error as e:
            return None, str(e)