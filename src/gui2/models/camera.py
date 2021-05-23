# database
from tinydb import TinyDB, Query
from tinydb.queries import where
from tinydb.operations import delete

class Camera_m:

    db = None

    def __init__(self):
        self.db = TinyDB('database/camera.json')
        #self.init_data()
        pass

    def init_data(self):
        # create sample data
        '''
        {
            "id": 1,
            "ip": "xxx.xxx.xxx.xxx",
            "username": "username",
            "password": "password",
            "status": 1,
        }
        '''
        self.db.insert({'id': 1, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 2, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 3, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 4, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 5, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 6, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 7, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 8, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 9, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 10, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 11, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 12, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 13, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 14, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 15, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 16, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 17, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 18, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 19, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        self.db.insert({'id': 20, 'ip': '192.168.13.100', 'username': 'admin', 'password': '215802', 'status': 1})
        
    def list(self):
        return (self.db.all())

    def getmaxid(self):
        id = 0
        rows = self.db.all()
        for row in rows:
            if row["id"] > id:
                id = row["id"]
        return id

    def get(self, id):
        q_camera = Query()
        row = self.db.get(q_camera.id == id)
        if row:
            return row
        else:
            return None

    def insert(self, row):
        self.db.insert(row)
        q_camera = Query()
        row = self.get(row["id"])
        if row:
            return True
        else:
            return False

    def update(self, row):
        if row:
            q_camera = Query()
            self.db.update(row, q_camera.id == row["id"])
            return True
        else:
            return False

    def delete(self, doc_id, id):
        self.db.remove(doc_ids=[doc_id])

        row = self.get(id)
        if row:
            return False
        else:
            return True