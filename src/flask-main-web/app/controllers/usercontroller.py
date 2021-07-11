from flask import render_template, request
from app import app

# database
from app.models.user import User_m

@app.route('/user/user', methods = ['GET'])
def settinguser():

    user_m = User_m()
    users = user_m.list()
    return render_template('/user/user.html', title="CMS - User", description="", users=users)


@app.route('/user/adduser', methods = ['POST'])
def adduser():
    data = request.json
    user_m = User_m()
    result, message = user_m.insert(data["username"], data["password"], data["name"], data["isadmin"], "suli")
    return {
        "success": "1" if result else "0",
        "message": message
    }


@app.route('/user/edituser', methods = ['POST'])
def edituser():
    data = request.json
    user_m = User_m()
    result, message = user_m.update(data["userid"], data["password"], data["name"], data["isadmin"], "suli")
    return {
        "success": "1" if result else "0",
        "message": message
    }


@app.route('/user/deleteuser', methods = ['POST'])
def deleteuser():
    data = request.json
    user_m = User_m()
    result, message = user_m.delete(data["userid"], "suli")
    return {
        "success": "1" if result else "0",
        "message": message
    }

