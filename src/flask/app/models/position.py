from tinydb import TinyDB, Query
from tinydb.queries import where
from tinydb.operations import delete

import os
from app.settings import DATABASE_PATH

class PositionDB:
    db = None

    def __init__(self) -> None:
        self.db = TinyDB(os.path.join(DATABASE_PATH, 'position.json'))
        

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
        query = Query()
        row = self.db.get(query.id == id)
        if row:
            return row
        else:
            return None


    def insert(self, row):
        self.db.insert(row)
        row = self.get(row["id"])
        if row:
            return True
        else:
            return False

    
    def update(self, row):
        if row:
            query = Query()
            self.db.update(row, query.id == row["id"])
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
