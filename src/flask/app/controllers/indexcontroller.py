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
from app.models.user import User_m

@app.route('/<uuid:sessionid>', methods = ['GET'])
def index(sessionid):

        print(sessionid)

        # validate the sessionid
        user_m = User_m()
        user = user_m.get_fromsession(sessionid)
        if user:
                session.pop('user', None)
                session.pop('sessionid', None)
                session['user'] = user
                session['sessionid'] = sessionid
                #print(session['user'])
                
                title = ""
                return render_template(
                        'index.html', 
                        title=title,
                        description="")
        else:
                redirect(url_for('error'))


@app.route('/login/<uuid:sessionid>', methods = ['GET'])
def login(sessionid):
        # validate the sessionid
        user_m = User_m()
        user = user_m.get_fromsession(sessionid)
        if user:
                session['user'] = user
                session['sessionid'] = sessionid
        
        return {
                "success": "1" if user else "0",
                "sessionid": sessionid
        }


@app.route('/logout', methods = ['GET'])
def logout():
        session.pop('user', None)
        session.pop('sessionid', None)
        return {
                "success": "1"
        }


@app.route('/error')
def error():
        return render_template('error.html')