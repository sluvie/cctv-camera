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
                g.user = user


@app.route('/', methods = ['GET'])
@app.route("/index")
def index():
        # auth page
        if not g.user:
                return redirect(url_for('login'))

        camera_m = Camera_m()
        cameras = camera_m.list()
        return render_template('index.html', title="Camera Management System", description="", cameras=cameras)


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
                        return redirect(url_for('index'))
                
                return redirect(url_for('login'))

        return render_template('login.html', title="Login - CMS", description="")


@app.route('/logout', methods = ['GET'])
def logout():
        session.pop('user', None)
        g.user = None
        return redirect(url_for('login'))