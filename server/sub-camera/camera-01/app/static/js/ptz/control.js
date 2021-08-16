$(document).ready(function () {
    console.log("Ready.");

    $("#btn_stopvideo").prop('disabled', true);
    $("#btn_recordvideo").prop('disabled', false);  
})




/* navigation camera */

$("#btn_left").click(function () {
    console.log("left");
    $.get("/ptz/left/5", function (data) {
        console.log(data);
    });
});

$("#btn_right").click(function () {
    console.log("right");
    $.get("/ptz/right/5", function (data) {
        console.log(data);
    });
});

$("#btn_up").click(function () {
    console.log("up");
    $.get("/ptz/up/5", function (data) {
        console.log(data);
    });
});

$("#btn_down").click(function () {
    console.log("down");
    $.get("/ptz/down/5", function (data) {
        console.log(data);
    });
});

$("#btn_stop").click(function () {
    console.log("stop");
    $.get("/ptz/stop", function (data) {
        console.log(data);
    });
});

/* MOVE BASED DEGREE */

$(document).on("click", ".btn-input-up", function(){
    console.log("input up");
    var input_comp = $(this).data("compid");
    var value = parseFloat($("#" + input_comp).val());
    value = value + 0.5;
    $("#" + input_comp).val(value);
});

$(document).on("click", ".btn-input-down", function(){
    console.log("input down");
    var input_comp = $(this).data("compid");
    var value = parseFloat($("#" + input_comp).val());
    value = value - 0.5;
    $("#" + input_comp).val(value);
});

$("#btn_left_degree").click(function () {
    console.log("left degree");
    var speed = $("#tx_left_degree").val()
    $.get("/ptz/left/" + speed, function (data) {
        console.log(data);
        setTimeout(function () {
            $.get("/ptz/stop", function () { });
        }, 5000);
    });
});

$("#btn_right_degree").click(function () {
    console.log("right degree");
    var speed = $("#tx_right_degree").val()
    $.get("/ptz/right/" + speed, function (data) {
        console.log(data);
        setTimeout(function () {
            $.get("/ptz/stop", function () { });
        }, 5000);
    });
});

$("#btn_up_degree").click(function () {
    console.log("up degree");
    var speed = $("#tx_up_degree").val()
    $.get("/ptz/up/" + speed, function (data) {
        console.log(data);
        setTimeout(function () {
            $.get("/ptz/stop", function () { });
        }, 5000);
    });
});

$("#btn_down_degree").click(function () {
    console.log("down degree");
    var speed = $("#tx_down_degree").val()
    $.get("/ptz/down/" + speed, function (data) {
        console.log(data);
        setTimeout(function () {
            $.get("/ptz/stop", function () { });
        }, 5000);
    });
});

/* END OF MOVE BASED DEGREE */


/* ZOOM IN / OUT */

$("#btn_zoomin").click(function () {
    console.log("zoomin");
    $.get("/ptz/zoomin", function (data) {
        console.log(data);
    });
});

$("#btn_zoomout").click(function () {
    console.log("zoomout");
    $.get("/ptz/zoomout", function (data) {
        console.log(data);
    });
});

/* END ZOOM IN / OUT */


/* SAVE LOAD POSITION */

$("#btn_showsaveposition").click(function () {
    console.log("show save position");
    $("#position-name").val("")
    $("#savepositionModal").modal('show');
});


$("#btn_showloadposition").click(function () {
    console.log("show load position");

    $.LoadingOverlay("show");
    $.ajax({
        type: "GET",
        url: url_camera_position_list,
        contentType: 'application/json',
        dataType: 'json',
        async: true,
        error: function () {
            $.LoadingOverlay("hide");
            Swal.fire("Error", '', 'error');
        },
        success: function (data) {
            if (data.success) {
                if (data.success == "1") {
                    var list = data.data;
                    index = 1;
                    $("#position-list").html("");
                    list.forEach(element => {
                        var content =
                            "<div class='row mt-2'> " +
                            "    <div class='col-1'>" + index + "</div> " +
                            "    <div class='col-7'>" + element.positionname + "</div> " +
                            "    <div class='col-4'> " +
                            "        <div class='row'> " +
                            "            <div class='col-6'> " +
                            "                <button class='btn btn-primary' data-positionnumber='" + element.positionnumber + "' onclick='gotoposition(this);'>移動</button> " +
                            "            </div> " +
                            "            <div class='col-6'> " +
                            "                <button class='btn btn-danger' data-positionnumber='" + element.positionnumber + "' data-camerapositionid='" + element.camerapositionid + "' onclick='deleteposition(this);'>delete</button> " +
                            "            </div> " +
                            "        </div> " +
                            "    </div> " +
                            "</div>";

                        $("#position-list").append(content);
                        index++;
                    });

                    $("#loadpositionModal").modal('show');
                    $.LoadingOverlay("hide");
                }
                else {
                    Swal.fire(data.message, '', 'error');
                }
            } else {
                Swal.fire("Failed to load position", '', 'error');
            }
        }
    });
});


$("#btn_saveposition").click(function () {
    console.log("save position");
    var data = {
        "positionname": $("#position-name").val()
    }

    $.LoadingOverlay("show");
    $.ajax({
        type: "POST",
        url: url_camera_position_add,
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        async: false,
        error: function () {
            $.LoadingOverlay("hide");
            Swal.fire("Error", '', 'error');
        },
        success: function (data) {
            console.log(data);
            $.LoadingOverlay("hide");
            if (data.success) {
                if (data.success == "1") {
                    $.get(url_preset_set + "/" + data.positionnumber, function (setdata) {
                        console.log(setdata);
                        $("#loadpositionModal").modal("hide");
                    });
                    $("#savepositionModal").modal('hide');
                }
                else {
                    Swal.fire(data.message, '', 'error');
                }
            } else {
                Swal.fire("Failed to add position", '', 'error');
            }
        }
    });
});


function deleteposition(evt) {
    console.log("delete position");
    var camerapositionid = evt.getAttribute("data-camerapositionid");
    var positionnumber = evt.getAttribute("data-positionnumber");
    var data = {
        "camerapositionid": camerapositionid
    }

    $.LoadingOverlay("show");
    $.ajax({
        type: "POST",
        url: url_camera_position_delete,
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        async: true,
        error: function () {
            $.LoadingOverlay("hide");
            Swal.fire("Error", '', 'error');
        },
        success: function (data) {
            $.LoadingOverlay("hide");
            if (data.success) {
                if (data.success == "1") {
                    $.get(url_preset_remove + "/" + positionnumber, function (data) {
                        console.log(data);
                    });
                    $("#loadpositionModal").modal('hide');
                }
                else {
                    Swal.fire(data.message, '', 'error');
                }
            } else {
                Swal.fire("Failed to delete position", '', 'error');
            }
        }
    });
}


function gotoposition(evt) {
    console.log("goto position");
    var positionnumber = evt.getAttribute("data-positionnumber");

    $.get(url_preset_goto + "/" + positionnumber, function (data) {
        console.log(data);
        $("#loadpositionModal").modal("hide");
    });
}

/* END SAVE LOAD POSITION */






/* CAPTURE */
// snapshot
$("#btn_captureimage").click(function () {
    console.log("capture image");

    $.ajax({
        type: "GET",
        url: "/ptz/captureimage",
        async: false,
        error: function () {
            $.LoadingOverlay("hide");
            Swal.fire("Error", '', 'error');
        },
        success: function (data) {
            $.LoadingOverlay("hide");
            var a = document.createElement("a"); //Create <a>
            a.href = "data:image/jpeg;base64," + data; //Image Base64 Goes here
            a.download = "snapshot.jpg"; //File name Here
            a.click(); //Downloaded file
        }
    });
});

// record
$("#btn_recordvideo").click(function () {
    console.log("record video");

    // var url = window.location.href + "record_status";
    $(this).prop('disabled', true);
    $("#btn_stopvideo").prop('disabled', false);
    
    // disable download link
    //var downloadLink = document.getElementById("download");
    //downloadLink.text = "";
    //downloadLink.href = "";

    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);
        }
    }
    xhr.open("POST", "/ptz/record_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ status: "true" }));
});

// stop record
$("#btn_stopvideo").click(function () {
    console.log("stop record");
    
    $(this).prop('disabled', true);
    $("#btn_recordvideo").prop('disabled', false);   

    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);

            // enable download link
            //var downloadLink = document.getElementById("download");
            //downloadLink.text = "Download Video";
            //downloadLink.href = "/static/video.avi";
        }
    }
    xhr.open("POST", "/ptz/record_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ status: "false" }));
});

/* END OF CAPTURE */