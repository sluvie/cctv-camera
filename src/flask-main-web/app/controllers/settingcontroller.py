from flask import (
    render_template, 
    g,
    request,
    redirect,
    url_for)
from app import app

# database
from app.models.camera import Camera_m

@app.route('/setting/camera', methods = ['GET'])
def settingcamera():
    # auth page
    if not g.user:
            return redirect(url_for('login'))

    camera_m = Camera_m()
    cameras = camera_m.list()
    return render_template('/setting/camera.html', title="CMS - Setting Camera", description="", cameras=cameras)


@app.route('/setting/addcamera', methods = ['POST'])
def addcamera():
    # auth page
    if not g.user:
            return redirect(url_for('login'))

    data = request.json
    camera_m = Camera_m()
    result, message = camera_m.insert(data["ip"], data["port"], data["rtspport"], data["username"], data["password"], "suli")
    return {
        "success": "1" if result else "0",
        "message": message
    }


@app.route('/setting/editcamera', methods = ['POST'])
def editcamera():
    # auth page
    if not g.user:
            return redirect(url_for('login'))

    data = request.json
    camera_m = Camera_m()
    result, message = camera_m.update(data["cameraid"], data["ip"], data["port"], data["rtspport"], data["username"], data["password"], "suli")
    return {
        "success": "1" if result else "0",
        "message": message
    }


@app.route('/setting/deletecamera', methods = ['POST'])
def deletecamera():
    # auth page
    if not g.user:
            return redirect(url_for('login'))

    data = request.json
    camera_m = Camera_m()
    result, message = camera_m.delete(data["cameraid"])
    return {
        "success": "1" if result else "0",
        "message": message
    }


@app.route("/setting/updatecameraonoff", methods = ['POST'])
def updatecamera_onoff():
    # auth page
    if not g.user:
            return redirect(url_for('login'))
            
    data = request.json
    camera_m = Camera_m()
    result, message = camera_m.update_onoff(data["cameraid"], data["onoff"], "suli")
    return {
        "success": "1" if result else "0",
        "message": message
    }


