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

    def readone_docker(self, dockername):
        try:
            cur = self.conn.cursor()
            query = "select cameraid, ip, webport, rtspport, username, password, companyname, placename, positionorder from t_camera where dockername=%s"
            cur.execute(query, (dockername, ))
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
                        'companyname': row[6],
                        'placename': row[7],
                        'positionorder': row[8]
                        
                    }
                return result, ""
        except psycopg2.Error as e:
            return None, str(e)