$(document).ready(function () {
    console.log("Ready.");
    $('#tbl-main').DataTable();
})


$("#btn_saveuser").click(function() {
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
                alert("failed to add user")
            }
        }
    });
});


$("#btn_edituser").click(function() {
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
                alert("failed to edit user")
            }
        }
    });
});


$("#btn_deleteuser").click(function() {
    console.log("delete user.");

    var data = {
        "userid": $(this).data("userid")
    };

    $.ajax({
        type: "POST",
        url: url_delete_user,
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
                alert("failed to edit user")
            }
        }
    });
});



$(".btn_infouser").click(function() {
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