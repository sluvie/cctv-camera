from flask import (
    render_template, 
    g,
    request,
    redirect,
    url_for)
from app import app

# execute bash
import subprocess

# database
from app.models.camera import Camera_m
from app.models.setting import Setting_m

# libraries
from app.libraries.docker_util import DockerUtil

@app.route('/setting/camera', methods = ['GET'])
def settingcamera():
    # auth page
    if not g.user:
            return redirect(url_for('login'))

    camera_m = Camera_m()
    cameras = camera_m.list()
    return render_template('/setting/camera.html', title="CMS - Setting Camera", description="", cameras=cameras)


@app.route('/setting/infocamera/<uuid:cameraid>', methods = ['GET'])
def informationcamera(cameraid):
    # auth page
    #if not g.user:
    #        return redirect(url_for('login'))

    camera_m = Camera_m()
    result, message = camera_m.readone(cameraid)
    return render_template('/setting/infocamera.html', title="CMS - Information Camera", description="", camera=result)


@app.route('/setting/readone', methods = ['POST'])
def camera_readone():
    # auth page
    if not g.user:
            return redirect(url_for('login'))
    
    user = g.user
    data = request.json
    camera_m = Camera_m()
    result, message = camera_m.readone(data["cameraid"])
    return {
            "success": "1" if result else "0",
            "message": message,
            "data": result
    }


@app.route('/setting/dockerinfo', methods = ['POST'])
def camera_docker():
    # auth page
    if not g.user:
            return redirect(url_for('login'))

    result = None
    return {
            "success": "1" if result else "0",
            "message": message,
            "data": result
    }


@app.route('/setting/addcamera', methods = ['POST'])
def addcamera():
    # auth page
    if not g.user:
            return redirect(url_for('login'))

    data = request.json
    camera_m = Camera_m()
    result, message = camera_m.insert(data["companyname"], data["placename"], data["positionorder"], data["startdate"], data["enddate"], data["ip"], data["port"], data["rtspport"], data["username"], data["password"], "suli")
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
    result, message = camera_m.update(data["cameraid"], data["companyname"], data["placename"], data["positionorder"], data["startdate"], data["enddate"], data["ip"], data["port"], data["rtspport"], data["username"], data["password"], "suli")
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


@app.route("/setting/generatecamera", methods = ['POST'])
def generatecamera():
    # auth page
    #if not g.user:
    #        return redirect(url_for('login'))
            
    data = request.json
    cameraid = data["cameraid"]
    
    # get docker port
    setting_m = Setting_m()
    data_setting, message = setting_m.readone_keytag("DOCKER", "PORT")
    startport = 0
    endport = 0
    if data_setting:
        startport = int(data_setting["tag1"])
        endport = int(data_setting["tag2"])

    # get all data camera
    camera_m = Camera_m()
    data_camera = camera_m.list()
    
    # scan available port
    availableport = 0
    for i in range(startport, endport):
        for x in range(0, len(data_camera)):
            if (data_camera[x]["dockerid"] != ""):
                if str(i) == data_camera[x]["dockerport"]:
                    availableport = i
        # if availableport == 0 then you can use the port
        if availableport == 0:
            availableport = i
            break

    
    # copy the master to folder port
    


    # prepare the config and server port


    # update docker camera
    result_update, message = camera_m.update_docker(cameraid, "test", "camera-random", availableport, "suli")
    print(message)

    # try to execute generate.sh    
    #subprocess.call('/home/sluvie/works/japan/cctv-camera/src/camera-docker/update.sh')    

    return {
        "success": "1",
        "message": ""
    }