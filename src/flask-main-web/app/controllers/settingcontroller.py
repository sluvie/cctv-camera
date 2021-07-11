from flask import render_template, request
from app import app

# database
from app.models.camera import Camera_m

@app.route('/setting/camera', methods = ['GET'])
def settingcamera():

    camera_m = Camera_m()
    cameras = camera_m.list()
    return render_template('/setting/camera.html', title="CMS - Setting Camera", description="", cameras=cameras)


@app.route('/setting/addcamera', methods = ['POST'])
def addcamera():
    data = request.json
    camera_m = Camera_m()
    result, message = camera_m.insert(data["ip"], data["port"], data["rtspport"], data["username"], data["password"], "suli")
    return {
        "success": "1" if result else "0",
        "message": message
    }


@app.route('/setting/deletecamera', methods = ['POST'])
def deletecamera():
    data = request.json
    camera_m = Camera_m()
    result, message = camera_m.delete(data["cameraid"])
    return {
        "success": "1" if result else "0",
        "message": message
    }


@app.route("/setting/updatecameraonoff", methods = ['POST'])
def updatecamera_onoff():
    data = request.json
    camera_m = Camera_m()
    result, message = camera_m.update_onoff(data["cameraid"], data["onoff"], "suli")
    return {
        "success": "1" if result else "0",
        "message": message
    }


