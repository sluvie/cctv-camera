let application_session_id = "";

$(document).ready(function () {
    console.log("Ready.");

    // get application session id
    application_session_id = Math.random().toString(36).substring(7).toUpperCase();
    $(".application-session-id").text(application_session_id);
})