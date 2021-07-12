$(document).ready(function () {
    console.log("Ready.");
    $('#tbl-main').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    });
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
            Swal.fire("Error", '', 'error')
        },
        success: function (data) {
            if (data.success) {
                if (data.success == "1") {
                    Swal.fire('Inserted!', '', 'success')
                    location.reload();
                } else {
                    Swal.fire(data.message, '', 'error')
                }
            } else {
                Swal.fire('Failed to add camera', '', 'error')
            }
        }
    });
});


$("#btn_editcamera").click(function () {
    console.log("edit camera.");

    var data = {
        "cameraid": $(this).data("cameraid"),
        "ip": $("#edit_ip").val(),
        "port": $("#edit_port").val(),
        "rtspport": $("#edit_rtsp-port").val(),
        "username": $("#edit_username").val(),
        "password": $("#edit_password").val()
    };

    $.ajax({
        type: "POST",
        url: url_edit_camera,
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        error: function () {
            Swal.fire("Error", '', 'error');
        },
        success: function (data) {
            if (data.success) {
                if (data.success == "1") {
                    Swal.fire('Updated!', '', 'success');
                    location.reload();
                } else {
                    Swal.fire(data.message, '', 'error');
                }
            } else {
                Swal.fire("Failed to edit camera", '', 'error');
            }
        }
    });
});


$("#btn_deletecamera").click(function() {
    console.log("delete camera.");

    var data = {
        "cameraid": $(this).data("cameraid")
    };

    Swal.fire({
        title: 'Do you want to delete the data?',
        icon: 'warning',
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: `Delete`,
        denyButtonText: `Don't delete`,
        cancelButtonText: '閉じる',
    }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            $.ajax({
                type: "POST",
                url: url_delete_camera,
                data: JSON.stringify(data),
                contentType: 'application/json',
                dataType: 'json',
                error: function () {
                    Swal.fire("Error", '', 'error')
                },
                success: function (data) {
                    if (data.success) {
                        if (data.success == "1") {
                            Swal.fire('Deleted!', '', 'success');
                            location.reload();
                        } else {
                            Swal.fire(data.message, '', 'error')
                        }
                    } else {
                        alert("failed to delete camera")
                    }
                }
            });
        } else if (result.isDenied) {
            Swal.fire('Data are not deleted', '', 'info');
        }
    });
});


$(".btn_infoeditcamera").click(function () {
    console.log("info edit camera.")

    camera_str = $(this).data("camera");
    camera_str = camera_str.replace(/\'/g, '"');
    // parse to json
    camera = JSON.parse(camera_str);

    // fill the data
    $("#edit_ip").val(camera.ip);
    $("#edit_port").val(camera.webport);
    $("#edit_rtsp-port").val(camera.rtspport);
    $("#edit_username").val(camera.username);
    $("#edit_password").val(camera.password);
    $("#btn_editcamera").data("cameraid", camera.cameraid);
    $("#btn_deletecamera").data("cameraid", camera.cameraid);
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