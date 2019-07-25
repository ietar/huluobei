function f1(){
    var form = document.getElementById('drawcards');
    var fd = new FormData(form);
    var xhr = new XMLHttpRequest();
    xhr.open('post', '/drawcards/');
    xhr.send(fd);
    xhr.onreadystatechange = function(){
        if(4 === xhr.readyState){
            if (xhr.status === 200 || xhr.status === 304){
                var ret = JSON.parse(xhr.responseText);
                document.getElementById('draw_result').innerHTML = ret.length;
            }
        }
    }
}