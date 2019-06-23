function func1(){
    form = document.getElementById('form1');
    fd = new FormData(form);
    var xhr = new XMLHttpRequest();
    xhr.open('post', '/shit/');
    xhr.send(fd);
    xhr.onreadystatechange = function(){
        if(xhr.readyState == 4){
            if (xhr.status == 200 || xhr.status == 304){
                ret = JSON.parse(xhr.responseText);
                document.getElementById('d1').innerHTML = ret.username;
                document.getElementById('d2').innerHTML = ret.email;
            }
        }
    }
}