$(document).ready(function () {
    console.log("Ready.");
})

$("#btn_left").click(function () {
    console.log("left");
    $.get("/ptz/left", function( data ) {
        console.log(data);
    });
});

$("#btn_right").click(function () {
    console.log("right");
    $.get("/ptz/right", function( data ) {
        console.log(data);
    });
});

$("#btn_up").click(function () {
    console.log("up");
    $.get("/ptz/up", function( data ) {
        console.log(data);
    });
});

$("#btn_down").click(function () {
    console.log("down");
    $.get("/ptz/down", function( data ) {
        console.log(data);
    });
});

$("#btn_stop").click(function () {
    console.log("stop");
    $.get("/ptz/stop", function( data ) {
        console.log(data);
    });
});

$("#btn_zoomin").click(function () {
    console.log("zoomin");
    $.get("/ptz/zoomin", function( data ) {
        console.log(data);
    });
});

$("#btn_zoomout").click(function () {
    console.log("zoomout");
    $.get("/ptz/zoomout", function( data ) {
        console.log(data);
    });
});

$("#btn_captureimage").click(function () {
    console.log("capture image");
    $.get("/ptz/captureimage", function( data ) {
        console.log(data);
    });
});


// use for load position
$("#btn_preset").click(function () {
    console.log("preset");
    $.get("/ptz/preset", function( data ) {
        console.log(data);
    });
});


$("#btn_saveposition").click(function () {
    console.log("save position");
    var positionname = $("#position-name").val();
    $.get("/ptz/saveposition/" + positionname, function( data ) {
        console.log(data);
    });
});