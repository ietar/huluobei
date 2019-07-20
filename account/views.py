import datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from account.models import User
import hmac
import random
from ietar_py_scripts import sendmail


# Create your views here.


def login(request):
    return render(request, 'account/login.html')


def logined(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = User.objects.filter(username__exact=username)
    if len(user) != 1:
        result = 'username failed'
        data = {
            'result': result,
        }
    else:
        shifted_password = hmac.new(key=bytes(user[0].salt, encoding='utf-8'), msg=bytes(password, encoding='utf-8'),
                                    digestmod='MD5').hexdigest()
        if shifted_password != User.objects.get(username__exact=username).password:
            result = 'password failed'
            data = {
                'result': result,
            }
        else:
            result = 'ok'
            request.session['user'] = {
                'username': user[0].username,
                'email': user[0].email,
                'img': str(user[0].img),
            }
            data = {
                'result': result,
                'username': user[0].username,
                'email': user[0].email,
            }
    # print(request.session)
    return render(request, 'account/logined.html', data)


def regist(request):
    data = {

    }
    return render(request, 'account/regist.html', data)


def registed(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    result = 'ok'
    user = User.objects.filter(username__exact=username)
    # print(len(user))
    if len(user) >= 1:
        result = 'not ok'
    else:
        newuser = User()
        newuser.username = username
        newuser.salt = str(random.randint(1, 100000)) + random.choice(username) + random.choice(username)
        newuser.password = hmac.new(key=bytes(newuser.salt, encoding='utf-8'), msg=bytes(password, encoding='utf-8'),
                                    digestmod='MD5').hexdigest()
        newuser.email = email
        dt = datetime.datetime.now()
        newuser.regist_time = dt
        newuser.access_time = dt
        newuser.save()

        user = User.objects.filter(username__exact=username)
        request.session['user'] = {
            'username': user[0].username,
            'email': user[0].email,
            'img': str(user[0].img),
        }
    data = {
        'result': result,
    }
    return render(request, 'account/registed.html', data)


def index(request):
    counts = len(User.objects.raw('select * from account_user;'))
    try:
        user = request.session['user']
    except KeyError:
        data = {
            'counts': counts,
        }
        return render(request, 'account/index.html', data)
    u = User.objects.filter(username__exact=user['username'])
    if len(u) == 1:
        u = u[0]
    else:
        request.session.clear()
        return redirect('/index/')

    upload = request.FILES.get('img')
    if upload:
        u.img = upload
    data = {
        'username': user['username'],
        'email': user['email'],
        'img': u.img,
        'counts': counts,
        'atime': u.access_time,
    }
    u.access_time = datetime.datetime.now()
    u.save()
    # print(request.session['user'])
    return render(request, 'account/index.html', data)


def logout(request):
    request.session.clear()
    return redirect(r'/index/')


def ajax_test(request):
    username = request.POST.get('askname')
    u = User.objects.filter(username__exact=username)
    data = {}
    if username:
        data['asked'] = 'yes'
    if u:
        data['username'] = u[0].username
        data['email'] = u[0].email
    return render(request, 'ajax_test.html', data)


def shit(request):
    username = request.POST.get('askname')
    u = User.objects.filter(username__exact=username)
    data = {}
    if username:
        data['asked'] = 'yes'
    else:
        return HttpResponse('这么访问不行啊')
    if u:
        data['username'] = u[0].username
        data['email'] = u[0].email
    else:
        data['username'] = '查无此人'
        data['email'] = '邮箱当然也查不到'
    return HttpResponse(JsonResponse(data))


def usercheck(request):
    username = request.POST.get('username')
    u = User.objects.filter(username__exact=username)
    u = len(u)
    return HttpResponse(JsonResponse({'username': u}))


def emailcheck(request):
    email = request.POST.get('email')
    u = User.objects.filter(email__exact=email)
    u = len(u)
    return HttpResponse(JsonResponse({'email': u}))


def resetpassword(request):
    return render(request, r'account/resetpassword.html')


def sendresetmail(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    if not username and not email:
        return HttpResponse('至少得填一个吧')
    ip = request.META.get('REMOTE_ADDR', 'unknown')
    if username:
        u = User.objects.filter(username__exact=username)
    else:
        u = User.objects.filter(email__exact=email)
    if len(u) != 1:
        return HttpResponse('不存在该用户')
    else:
        u = u[0]
        username = u.username
        salt = u.salt
        uid = u.id
        email = u.email
        temp = str(random.randint(1, 100000)) + random.choice(username) + random.choice(username)
        u.reset_password_salt = hmac.new(key=bytes(temp, encoding='utf-8'),
                                         msg=bytes(str(datetime.datetime.now()), encoding='utf-8'),
                                         digestmod='MD5').hexdigest()
        temp = u.reset_password_salt
        u.reset_time = datetime.datetime.now()
        u.save()
        m_email = u.email.split('@', 1)[0][:-4] + '****@' + u.email.split('@', 1)[1]
        msg = '''取回密码说明
        {username}， 这封信是由 {host} 发送的。

您收到这封邮件，是由于这个邮箱地址在 {host} 被登记为用户邮箱， 且该用户请求使用 Email 密码重置功能所致。

----------------------------------------------------------------------
重要！
----------------------------------------------------------------------

如果您没有提交密码重置的请求或不是 {host} 的注册用户，请立即忽略 并删除这封邮件。只有在您确认需要重置密码的情况下，才需要继续阅读下面的 内容。

----------------------------------------------------------------------
密码重置说明
----------------------------------------------------------------------

您只需在提交请求后的一小时内，通过点击下面的链接重置您的密码：
{url}
(如果上面不是链接形式，请将该地址手工粘贴到浏览器地址栏再访问)
在上面的链接所打开的页面中输入新的密码后提交，您即可使用新的密码登录网站了。您可以在用户控制面板中随时修改您的密码。

本请求提交者的 IP 为 {ip}

此致
{host} 管理团队. {host}
'''.format(username=u.username, host='http://www.ietar.xyz/', ip=ip,
           url='http://www.ietar.xyz/account/reset?resetsalt={}&id={}&salt={}'.format(temp, uid, salt))
        sendmail.sendresetpassword(message=msg,to=email)

    return HttpResponse('已成功发送找回邮件至 {}'.format(m_email))


def reset(request):
    data = {}
    resetsalt = request.GET.get('resetsalt')
    uid = request.GET.get('id')
    salt = request.GET.get('salt')
    u = User.objects.filter(id__exact=uid, reset_password_salt__exact=resetsalt, salt__exact=salt)
    if len(u) == 1:
        u = u[0]
        data['username'] = u.username
        request.session['user'] = {
            'username': u.username,
            'email': u.email,
            'img': str(u.img),
        }
    return render(request, r'account/reset.html', data)


def reset_done(request):
    try:
        username = request.session['user']['username']
    except KeyError:
        return HttpResponse('您从哪来的 session不对吧')
    password = request.POST.get('password')
    u = User.objects.filter(username__exact=username)[0]
    u.password = hmac.new(key=bytes(u.salt, encoding='utf-8'), msg=bytes(password, encoding='utf-8'),
                                    digestmod='MD5').hexdigest()
    u.save()
    return render(request, r'account/reset_done.html')
