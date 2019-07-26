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
function f2(){
    var iframe = document.getElementById('iframe1');
    iframe.src = "/drawcards/";
    iframe.width = 660;
    iframe.height = 120;
}
function f3(){
    var iframe = document.getElementById('iframe1');
    iframe.src = "";
    iframe.width = 0;
    iframe.height = 0;
}