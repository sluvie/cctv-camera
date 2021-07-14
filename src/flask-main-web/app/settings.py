from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/')

DATABASE_CONFIG = {
    "host": "katasaham.com",
    "port": 5432,
    "user": "camera",
    "password": "camera",
    "database": "cameradb"
}