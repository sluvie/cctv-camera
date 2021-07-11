from flask import render_template, Response
from app import app

# database
from app.models.camera import Camera_m

@app.route('/', methods = ['GET'])
def index():
        camera_m = Camera_m()
        cameras = camera_m.list()
        return render_template('index.html', title="Camera Management System", description="", cameras=cameras)


@app.route('/login', methods = ['GET'])
def login():
        return render_template('login.html', title="Login - CMS", description="")