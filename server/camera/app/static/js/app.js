$(document).ready(function () {
    console.log("Ready.");
})


$(".btn_onoff").click(function() {
    console.log("turn on / off.")

    // mybutton
    mybutton = $(this);

    cameraid = $(this).data("cameraid");
    cameraonoff = $(this).data("cameraonoff");
    cameraonoff = (cameraonoff == 0 ? 1 : 0);

    var data = {
        "cameraid": cameraid,
        "onoff": cameraonoff
    };

    $.LoadingOverlay("show");
    $.ajax({
        type: "POST",
        url: url_update_camera_onoff,
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        async: false,
        error: function () {
            alert("error");
        },
        success: function (data) {
            if (data.success) {
                if (data.success == "1") {
                    if (cameraonoff == 1) {
                        mybutton.text('オフ');
                        mybutton.removeClass("btn-success");
                        mybutton.addClass("btn-danger");
                        //$("#img_camera_" + camera.cameraid).attr('src', 'http://localhost:8081/ptz/video_feed');
                        location.reload();
                    }
                    else {                        
                        mybutton.text('オン');
                        mybutton.removeClass("btn-danger");
                        mybutton.addClass("btn-success");
                        location.reload();
                        //$("#img_camera_" + camera.cameraid).attr('src', '/static/img/no-cctv.png');
                    }
                    // set back to button
                    mybutton.data("camera", JSON.stringify(camera));
                } else {
                    alert(data.message);
                }
            } else {
                alert("failed to turn on / off camera")
            }
            $.LoadingOverlay("hide");
        }
    });
});