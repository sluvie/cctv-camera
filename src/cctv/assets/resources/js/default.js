let application_session_id = "";

$(document).ready(function () {
    console.log("Ready.");

    // get application session id
    application_session_id = Math.random().toString(36).substring(7).toUpperCase();
    $(".application-session-id").text(application_session_id);

    // default nested tree
    nested_tree("caret");
})


/**-------------
 * Nested Tree
-------------*/
function nested_tree(element_id) {
    var toggler = document.getElementsByClassName(element_id);
    var i;

    for (i = 0; i < toggler.length; i++) {
    toggler[i].addEventListener("click", function() {
        this.parentElement.querySelector(".nested").classList.toggle("active");
    });
    }
}