from flask import (
    render_template, 
    g,
    request,
    session,
    redirect,
    url_for)
from app import app

# database
from app.models.user import User_m

@app.route('/user/user', methods = ['GET'])
def browseuser():
    # auth page
    if not g.user:
            return redirect(url_for('login'))

    user_m = User_m()
    users = user_m.list()
    users = [] if users == None else users

    # user session
    user_session = g.user
    sessionid = session['sessionid']

    return render_template('/user/user.html', title="CMS - User", description="", users=users, user_session=user_session, sessionid=sessionid)


@app.route('/user/readone', methods = ['POST'])
def user_readone():
        # auth page
        if not g.user:
                return redirect(url_for('login'))
        
        user = g.user
        data = request.json
        user_m = User_m()
        result, message = user_m.readone(data["userid"])
        return {
                "success": "1" if result else "0",
                "message": message,
                "data": result
        }


@app.route('/user/adduser', methods = ['POST'])
def adduser():
    # auth page
    if not g.user:
            return redirect(url_for('login'))

    data = request.json
    user_m = User_m()
    result, message = user_m.insert(data["username"], data["password"], data["name"], data["isadmin"], "suli")
    return {
        "success": "1" if result else "0",
        "message": message
    }


@app.route('/user/edituser', methods = ['POST'])
def edituser():
    # auth page
    if not g.user:
            return redirect(url_for('login'))

    data = request.json
    user_m = User_m()
    result, message = user_m.update(data["userid"], data["password"], data["name"], data["isadmin"], "suli")
    return {
        "success": "1" if result else "0",
        "message": message
    }


@app.route('/user/deleteuser', methods = ['POST'])
def deleteuser():
    # auth page
    if not g.user:
            return redirect(url_for('login'))

    data = request.json
    user_m = User_m()
    result, message = user_m.delete(data["userid"], "suli")
    return {
        "success": "1" if result else "0",
        "message": message
    }

