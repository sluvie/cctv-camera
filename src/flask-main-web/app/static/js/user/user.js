$(document).ready(function () {
    console.log("Ready.");
    $('#tbl-main').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    });
})


$("#btn_saveuser").click(function () {
    console.log("save user.");

    var data = {
        "username": $("#username").val(),
        "password": $("#password").val(),
        "name": $("#nameuser").val(),
        "isadmin": $('#isadmin').is(":checked") ? 1 : 0
    };

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
                    Swal.fire('Inserted!', '', 'success');
                    location.reload();
                } else {
                    Swal.fire(data.message, '', 'error');
                }
            } else {
                Swal.fire("Failed to add user", '', 'error');
            }
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
                    Swal.fire('Updated!', '', 'success');
                    location.reload();
                } else {
                    Swal.fire(data.message, '', 'error');
                }
            } else {
                Swal.fire("Failed to edit user", '', 'error');
            }
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
                }
            });
        } else if (result.isDenied) {
            Swal.fire('Data are not deleted', '', 'info');
        }
    });
});



$(".btn_infouser").click(function () {
    console.log("info user.")

    user_str = $(this).data("user");
    user_str = user_str.replace(/\'/g, '"');
    // parse to json
    user = JSON.parse(user_str);

    // fill the data
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
});