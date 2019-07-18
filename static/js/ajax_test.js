function func1(){
    var form = document.getElementById('form1');
    var fd = new FormData(form);
    var xhr = new XMLHttpRequest();
    xhr.open('post', '/shit/');
    xhr.send(fd);
    xhr.onreadystatechange = function(){
        if(4 === xhr.readyState){
            if (xhr.status === 200 || xhr.status === 304){
                var ret = JSON.parse(xhr.responseText);
                document.getElementById('d1').innerHTML = ret.username;
                document.getElementById('d2').innerHTML = ret.email;
            }
        }
    }
}