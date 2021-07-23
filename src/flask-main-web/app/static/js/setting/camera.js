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
        "companyname": $("#companyname").val(),
        "placename": $("#placename").val(),
        "positionorder": $("#positionorder").val(),
        "ip": $("#ip").val(),
        "port": $("#port").val(),
        "rtspport": $("#rtsp-port").val(),
        "username": $("#username").val(),
        "password": $("#password").val()
    };

    $.LoadingOverlay("show");
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
                    $.LoadingOverlay("hide");
                    location.reload();
                } else {
                    Swal.fire(data.message, '', 'error')
                }
            } else {
                Swal.fire('Failed to add camera', '', 'error')
            }
            $.LoadingOverlay("hide");
        }
    });
});


$("#btn_editcamera").click(function () {
    console.log("edit camera.");

    var data = {
        "cameraid": $(this).data("cameraid"),
        "companyname": $("#edit_companyname").val(),
        "placename": $("#edit_placename").val(),
        "positionorder": $("#edit_positionorder").val(),
        "ip": $("#edit_ip").val(),
        "port": $("#edit_port").val(),
        "rtspport": $("#edit_rtsp-port").val(),
        "username": $("#edit_username").val(),
        "password": $("#edit_password").val()
    };

    $.LoadingOverlay("show");
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
                    $.LoadingOverlay("hide");
                    location.reload();
                } else {
                    Swal.fire(data.message, '', 'error');
                }
            } else {
                Swal.fire("Failed to edit camera", '', 'error');
            }
            $.LoadingOverlay("hide");
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
            $.LoadingOverlay("show");
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
                            $.LoadingOverlay("hide");
                            Swal.fire('Deleted!', '', 'success');
                            location.reload();
                        } else {
                            Swal.fire(data.message, '', 'error')
                        }
                    } else {
                        alert("failed to delete camera")
                    }
                    $.LoadingOverlay("hide");
                }
            });
        } else if (result.isDenied) {
            Swal.fire('Data are not deleted', '', 'info');
        }
    });
});


$(".btn_infoeditcamera").click(function () {
    console.log("info edit camera.")

    var cameraid = $(this).data("cameraid");
    var data = {
        "cameraid": cameraid,
    };
    $.LoadingOverlay("show");
    $.ajax({
        type: "POST",
        url: url_readone_camera,
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        error: function () {
            Swal.fire("Error", '', 'error');
        },
        success: function (data) {
            if (data.success) {
                if (data.success == "1") {
                    // fill the data
                    var camera = data.data;
                    $("#edit_companyname").val(camera.companyname);
                    $("#edit_placename").val(camera.placename);
                    $("#edit_positionorder").val(camera.positionorder);
                    $("#edit_ip").val(camera.ip);
                    $("#edit_port").val(camera.webport);
                    $("#edit_rtsp-port").val(camera.rtspport);
                    $("#edit_username").val(camera.username);
                    $("#edit_password").val(camera.password);
                    $("#btn_editcamera").data("cameraid", camera.cameraid);
                    $("#btn_deletecamera").data("cameraid", camera.cameraid);
                    $("#editcameraModal").modal('show');
                } else {
                    Swal.fire(data.message, '', 'error');
                }
            } else {
                Swal.fire("Failed to get data camera", '', 'error');
            }
            $.LoadingOverlay("hide");
        }
    });
});


$(".btn_infocamera").click(function() {
    console.log("info camera.")

    var cameraid = $(this).data("cameraid");
    var data = {
        "cameraid": cameraid,
    };
    $.LoadingOverlay("show");
    $.ajax({
        type: "POST",
        url: url_readone_camera,
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        error: function () {
            Swal.fire("Error", '', 'error');
        },
        success: function (data) {
            if (data.success) {
                if (data.success == "1") {
                    // fill the data
                    var camera = data.data;
                    $("#label_detail_camera_companyname").text(camera.companyname);
                    $("#label_detail_camera_placename").text(camera.placename);
                    $("#label_detail_camera_positionorder").text(camera.positionorder);
                    $("#label_detail_camera_ip").text(camera.ip);
                    $("#label_detail_camera_port").text(camera.webport);
                    $("#label_detail_camera_rtsp_port").text(camera.rtspport);
                    $("#label_detail_camera_username").text(camera.username);
                    $("#label_detail_camera_password").text(camera.password);
                    $("#btn_deletecamera").data("cameraid", camera.cameraid);
                    $("#detailcameraModal").modal('show');
                } else {
                    Swal.fire(data.message, '', 'error');
                }
            } else {
                Swal.fire("Failed to get data camera", '', 'error');
            }
            $.LoadingOverlay("hide");
        }
    });
});