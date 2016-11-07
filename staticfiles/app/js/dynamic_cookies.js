
function home_page_alert() {
	var name="homepagealertstatus"
	var value=0
	var days=15
	var date, expires;
    if (days) {
        date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        expires = "; expires="+date.toGMTString();
    } else {
        expires = "";
    }
    document.cookie = name+"="+value+expires;
}
