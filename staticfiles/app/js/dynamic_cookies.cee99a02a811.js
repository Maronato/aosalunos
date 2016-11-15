

var info_cookie = new String("info_cookie")
$(function() {
    console.log(info_cookie);
    var cookie = getCookie(info_cookie);
    console.log(cookie);
    if (cookies) {
        $("#info-panel").css("display", "block");
        $("#info-content").html(cookie.substring(1, cookie.length - 1));
    }
});

function hide_info() {
    $("#info-panel").css("display", "none");
    $.removeCookie(info_cookie, { path: '/' });
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length,c.length);
        }
    }
    return "";
}
