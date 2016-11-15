

var info_cookie = new String("info_cookie")
$(function() {
    var cookie = getCookie(info_cookie);
    if (cookie != null) {
        $("#info-panel").css("display", "block");
        $("#info-content").html(cookie.substring(1, cookie.length - 1));
    }
});

function hide_info() {
    $("#info-panel").css("display", "none");
    $.removeCookie(info_cookie, { path: '/' });
}

function getCookie(name) {
    var dc = document.cookie;
    var prefix = name + "=";
    var begin = dc.indexOf("; " + prefix);
    if (begin == -1) {
        begin = dc.indexOf(prefix);
        if (begin != 0) return null;
    }
    else
    {
        begin += 2;
        var end = document.cookie.indexOf(";", begin);
        if (end == -1) {
        end = dc.length;
        }
    }
    // because unescape has been deprecated, replaced with decodeURI
    //return unescape(dc.substring(begin + prefix.length, end));
    return decodeURI(dc.substring(begin + prefix.length, end));
}
