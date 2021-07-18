$(document).ready(function () {
    console.log("Ready.");
    $('#tbl-main').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    });
});


$("#btn_saveuser").click(function () {
    console.log("save user.");

    var data = {
        "username": $("#username").val(),
        "password": $("#password").val(),
        "name": $("#nameuser").val(),
        "isadmin": $('#isadmin').is(":checked") ? 1 : 0
    };

    $.LoadingOverlay("show");
    $.ajax({
        type: "POST",
        url: url_add_user,
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        error: function () {
            Swal.fire("Error", '', 'error');
        },
        success: function (data) {
            if (data.success) {
                if (data.success == "1") {
                    //Swal.fire('Inserted!', '', 'success');
                    location.reload();
                } else {
                    Swal.fire(data.message, '', 'error');
                }
            } else {
                Swal.fire("Failed to add user", '', 'error');
            }
            $.LoadingOverlay("hide");
        }
    });
});


$("#btn_edituser").click(function () {
    console.log("edit user.");

    var data = {
        "userid": $(this).data("userid"),
        "password": $("#edit_password").val(),
        "name": $("#edit_nameuser").val(),
        "isadmin": $('#edit_isadmin').is(":checked") ? 1 : 0
    };

    $.LoadingOverlay("show");
    $.ajax({
        type: "POST",
        url: url_edit_user,
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        error: function () {
            Swal.fire("Error", '', 'error');
        },
        success: function (data) {
            if (data.success) {
                if (data.success == "1") {
                    //Swal.fire('Updated!', '', 'success');
                    location.reload();
                } else {
                    Swal.fire(data.message, '', 'error');
                }
            } else {
                Swal.fire("Failed to edit user", '', 'error');
            }
            $.LoadingOverlay("hide");
        }
    });
});


$("#btn_deleteuser").click(function () {
    console.log("delete user.");

    var data = {
        "userid": $(this).data("userid")
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
                url: url_delete_user,
                data: JSON.stringify(data),
                contentType: 'application/json',
                dataType: 'json',
                error: function () {
                    Swal.fire("Error", '', 'error');
                },
                success: function (data) {
                    if (data.success) {
                        if (data.success == "1") {
                            Swal.fire('Deleted!', '', 'success');
                            location.reload();
                        } else {
                            Swal.fire(data.message, '', 'error');
                        }
                    } else {
                        Swal.fire('Failed to delete user', '', 'info');
                    }
                    $.LoadingOverlay("hide");
                }
            });
        } else if (result.isDenied) {
            Swal.fire('Data are not deleted', '', 'info');
        }
    });
});



$(".btn_infouser").click(function () {
    console.log("info user.")

    var userid = $(this).data("userid");
    var data = {
        "userid": userid,
    };
    $.LoadingOverlay("show");
    $.ajax({
        type: "POST",
        url: url_readone_user,
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
                    var user = data.data;
                    $("#label_edit_username").text(user.username);
                    $("#edit_password").val(user.password);
                    $("#edit_nameuser").val(user.name);
                    if (user.isadmin == 1) {
                        $("#edit_isadmin").prop('checked', true);
                    }
                    else {
                        $("#edit_isadmin").prop('checked', false);
                    }
                    $("#btn_edituser").data("userid", user.userid);
                    $("#btn_deleteuser").data("userid", user.userid);
                    $("#edituserModal").modal('show');
                } else {
                    Swal.fire(data.message, '', 'error');
                }
            } else {
                Swal.fire("Failed to get data project", '', 'error');
            }
            $.LoadingOverlay("hide");
        }
    });
});