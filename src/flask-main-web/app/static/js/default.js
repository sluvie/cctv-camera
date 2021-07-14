// camera
var url_readone_camera = "/setting/readone";
var url_add_camera = "/setting/addcamera";
var url_edit_camera = "/setting/editcamera";
var url_delete_camera = "/setting/deletecamera";
var url_update_camera_onoff = "/setting/updatecameraonoff";

// user
var url_readone_user = "/user/readone";
var url_add_user = "/user/adduser";
var url_edit_user = "/user/edituser";
var url_delete_user = "/user/deleteuser";

$(document).ready(function () {
    console.log("Ready.");
})

$.date = function (dateObject) {
    var d = new Date(dateObject);
    var day = d.getDate();
    var month = d.getMonth() + 1;
    var year = d.getFullYear();
    if (day < 10) {
        day = "0" + day;
    }
    if (month < 10) {
        month = "0" + month;
    }
    var date = year + "-" + month + "-" + day;

    return date;
};


$.datetime = function (dateObject) {
    var d = new Date(dateObject);
    var day = d.getDate();
    var month = d.getMonth() + 1;
    var year = d.getFullYear();
    var hour = d.getHours();
    var minute = d.getMinutes();
    var second = d.getSeconds();
    if (day < 10) {
        day = "0" + day;
    }
    if (month < 10) {
        month = "0" + month;
    }
    var date = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second;

    return date;
}