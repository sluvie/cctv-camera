var url_add_camera = "/setting/addcamera";

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
            console.log(data);
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