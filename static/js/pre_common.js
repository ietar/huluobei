function get_cookie(key){
    let r = document.cookie.match("\\b" + key + "=([^;]*)\\b");
    return r?r[1]:false
}

function int2ip(_int){
    _int = parseInt(_int);
    let r = [];
    for (let i=3;i>=0;i--){
        r.push((_int>>(8*i)) & 0xFF);
    }
    return r.join('.')
}

function utc2local(dateStr) {
    let date1 = new Date();
    let offsetMinute = date1.getTimezoneOffset();
    let offsetHours = offsetMinute / 60;
    let date2 = new Date(dateStr);
    date2.setHours(date2.getHours() - offsetHours);
    return date2;
}

function guid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        let r = Math.random()*16|0, v = c === 'x' ? r : (r&0x3|0x8);
        return v.toString(16);
    });
}
