from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/')
DATABASE_PATH = join(dirname(realpath(__file__)), 'database/')

DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "camera",
    "password": "camera",
    "database": "cameradb"
}