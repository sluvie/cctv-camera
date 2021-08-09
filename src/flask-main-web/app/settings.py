from os.path import join, dirname, realpath


DOWNLOADS_PATH = join(dirname(realpath(__file__)), 'downloads/')
UPLOADS_PATH = join(dirname(realpath(__file__)), 'uploads/')
UPLOADS_IMAGES_PATH = join(dirname(realpath(__file__)), 'uploads/images/')
UPLOADS_VIDEOS_PATH = join(dirname(realpath(__file__)), 'uploads/videos/')


DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5499,
    "user": "camera",
    "password": "camera",
    "database": "cameradb"
}