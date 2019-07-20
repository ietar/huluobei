function check(){
    if (document.getElementsByName('password')[0].value !== document.getElementsByName('repassword')[0].value) {
        alert("您两次输入的密码不一样！请重新输入.");
        document.getElementById("submit").disabled = true;
        document.getElementsByName('repassword').focus();
    }
    else{
        document.getElementById("submit").disabled = false;
    }
}

function usercheck(){
    var userinfo = document.getElementById('usercheckinfo');
    var username = document.getElementById('username');
    if (username.value === ''){
        return 0;
    }
    var form = document.getElementById('form1');
    var fd = new FormData(form);
    var xhr = new XMLHttpRequest();
    xhr.open('post', '/usercheck/');
    xhr.send(fd);
    xhr.onreadystatechange = function(){
        if(4 === xhr.readyState){
            if (xhr.status === 200 || xhr.status === 304){
                var ret = JSON.parse(xhr.responseText);
                if (ret.username){
                    userinfo.innerHTML = '× 用户名重复';
                    userinfo.style.color = 'red';
                    return 0;
                }
                else{
                    userinfo.innerHTML = '√ 未注册的用户名';
                    userinfo.style.color = 'green';
                    return 1;
                }
            }
        }
    }
}

function emailcheck(){
    var emailinfo = document.getElementById('emailcheckinfo');
    var email = document.getElementById('email');
    if (email.value === ''){
        return 0;
    }
    var form = document.getElementById('form1');
    var fd = new FormData(form);
    var xhr = new XMLHttpRequest();
    xhr.open('post', '/emailcheck/');
    xhr.send(fd);
    xhr.onreadystatechange = function(){
        if(4 === xhr.readyState){
            if (xhr.status === 200 || xhr.status === 304){
                var ret = JSON.parse(xhr.responseText);
                if (ret.email){
                    emailinfo.innerHTML = '× 邮箱重复';
                    emailinfo.style.color = 'red';
                    return 0;
                }
                else{
                    emailinfo.innerHTML = '√ 未注册的邮箱';
                    emailinfo.style.color = 'green';
                    return 1;
                }
            }
        }
    }
}