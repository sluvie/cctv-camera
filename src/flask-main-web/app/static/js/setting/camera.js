$(document).ready(function () {
    console.log("Ready.");
    $('#tbl-main').DataTable();
})


$("#btn_savecamera").click(function() {
    console.log("save camera.");

    var data = {
        "ip": $("#ip").val(),
        "port": $("#port").val(),
        "rtspport": $("#rtsp-port").val(),
        "username": $("#username").val(),
        "password": $("#password").val()
    };

    $.ajax({
        type: "POST",
        url: url_add_camera,
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        error: function () {
            alert("error");
        },
        success: function (data) {
            if (data.success) {
                if (data.success == "1") {
                    location.reload();
                } else {
                    alert(data.message);
                }
            } else {
                alert("failed to add camera")
            }
        }
    });
});


$("#btn_deletecamera").click(function() {
    console.log("delete camera.");

    var data = {
        "cameraid": $(this).data("cameraid")
    };
    console.log(data);

    $.ajax({
        type: "POST",
        url: url_delete_camera,
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        error: function () {
            alert("error");
        },
        success: function (data) {
            if (data.success) {
                if (data.success == "1") {
                    location.reload();
                } else {
                    alert(data.message);
                }
            } else {
                alert("failed to delete camera")
            }
        }
    });
});


$(".btn_infocamera").click(function() {
    console.log("info camera.")

    camera_str = $(this).data("camera");
    camera_str = camera_str.replace(/\'/g, '"');
    // parse to json
    camera = JSON.parse(camera_str);

    // fill the data
    $("#label_detail_camera_ip").text(camera.ip);
    $("#label_detail_camera_port").text(camera.webport);
    $("#label_detail_camera_rtsp_port").text(camera.rtspport);
    $("#label_detail_camera_username").text(camera.username);
    $("#label_detail_camera_password").text(camera.password);
    $("#btn_deletecamera").data("cameraid", camera.cameraid);
});