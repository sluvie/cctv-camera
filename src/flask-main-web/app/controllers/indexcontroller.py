from datetime import timedelta
from flask import (
        render_template, 
        g,
        request,
        session,
        redirect,
        url_for
)
from app import app

# database
from app.models.camera import Camera_m
from app.models.user import User_m
from app.models.setting import Setting_m

# docker
from app.libraries.docker_util import DockerUtil

import requests


'''
TODO:
update the session database every 10 minutes
'''
@app.before_request
def before_request():
        g.user = None
        if 'user' in session:
                # find user based on userid, update information user
                user = session['user']
                sessionid = session['sessionid']
                g.user = user

                user_m = User_m()
                user_m.update_session(sessionid)


@app.route('/', methods = ['GET'])
@app.route("/index")
def index():
        # auth page
        if not g.user:
                return redirect(url_for('login'))

        camera_m = Camera_m()
        cameras = camera_m.list()
        cameras = [] if cameras == None else cameras

        # get status docker
        try:
                dockerutil = DockerUtil()
                for row in cameras:
                        status = dockerutil.container_status(row['dockername'])
                        row["dockerstatus"] = 1 if status else 0
        except:
                print("there is no docker")

        # get base url
        setting_m = Setting_m()
        data_baseurl, message = setting_m.readone_keytag("SERVER", "BASEURL")
        baseurl = "/"
        if (data_baseurl):
                baseurl = data_baseurl["tag1"]

        # user session
        user_session = g.user
        sessionid = session['sessionid']

        return render_template('index.html', title="Camera Management System", description="", cameras=cameras, baseurl=baseurl, user_session=user_session, sessionid=sessionid)


@app.route('/login', methods = ['GET', 'POST'])
def login():

        if request.method == 'POST':
                session.pop('user', None)
                username = request.form['username']
                password = request.form['password']

                user_m = User_m()
                user = user_m.get(username)
                if user and user['password'] == password:
                        session['user'] = user
                        result_session = user_m.create_session(user["userid"], user["username"])
                        sessionid = ""
                        if result_session:
                                sessionid = user_m.get_sessionid(username)
                        session['sessionid'] = sessionid
                        
                        session.permanent = True
                        app.permanent_session_lifetime = timedelta(minutes=30) #  set the session expiration date 

                        return redirect(url_for('index'))
                
                return redirect(url_for('login'))

        return render_template('login.html', title="Login - CMS", description="")


@app.route('/logout', methods = ['GET'])
def logout():
        camera_m = Camera_m()
        cameras = camera_m.list()
        cameras = [] if cameras == None else cameras
        
        session.pop('user', None)
        session.pop('sessionid', None)
        g.user = None

        return redirect(url_for('login'))