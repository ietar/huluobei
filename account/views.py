import datetime
import random
import hmac
import re

from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.db import DatabaseError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django_redis import get_redis_connection

from account.models import User

from ietar_py_scripts import sendmail, get_ip, draw_cards_arknight

# Create your views here.
from utils.any import ip2int, get_client_ip


class LoginPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(to='/')
        return render(request, 'account/login.html')

    def post(self, request):
        e_data = {'error_info': '',
                  'return_page': '/login',
                  'return_text': '回登录页面'}
        dic = request.POST
        username = dic.get('username')
        password = dic.get('password')
        img_code = dic.get('img_code')
        uuid = dic.get('uuid')

        if not all((username, password, img_code, uuid)):
            e_data['error_info'] = f'param username: {username}, password: {password},' \
                f' img_code: {img_code}, uuid: {uuid} required'
            return render(request, 'common_error.html', e_data, status=403)

        redis_conn = get_redis_connection('verify_code')
        img_code_server = redis_conn.get(f'img_code_{uuid}')
        if not img_code_server:
            e_data['error_info'] = '图形验证码已过期'
            return render(request, 'common_error.html', e_data, status=403)
        if img_code_server.decode() != img_code:
            e_data['error_info'] = f'图形验证码不一致 {img_code_server.decode()} {img_code}'
            return render(request, 'common_error.html', e_data, status=403)

        user = authenticate(username=username, password=password)
        if user is None:
            e_data['error_info'] = f'authenticate failed'
            return render(request, 'common_error.html', e_data, status=403)
        login(request=request, user=user)
        user.login_ip = ip2int(get_client_ip(request))
        user.save()

        _next = request.GET.get('next')
        response = redirect(_next) if _next else redirect('/')
        # 用于页面user_info_bar展示用户信息
        cookie_expire = settings.__getattr__('COOKIE_EXPIRE') or 3600 * 24 * 7
        response.set_cookie(key='username', value=user.username, max_age=cookie_expire)
        return response


class RegisterPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(to='/')
        return render(request, 'account/register.html')

    def post(self, request):
        dic = request.POST  # from form
        e_data = {'error_info': '',
                  'return_page': '/register',
                  'return_text': '回注册页面'}
        # print(dic)
        username = dic.get('username')
        password = dic.get('password')
        password2 = dic.get('password2')
        email = dic.get('email')
        allow = dic.get('allow')
        uuid = dic.get('uuid')
        img_code = dic.get('img_code')
        sms_code = dic.get('sms_code')

        if not all((username, password, password2, email, allow, uuid, img_code)):
            e_data['error_info'] = 'param username, password, password2, mobile, allow, uuid, img_code required'
            return render(request, 'common_error.html', e_data, status=403)
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            e_data['error_info'] = '5-20字符的username'
            return render(request, 'common_error.html', e_data, status=403)
        if not re.match(r'^.{8,20}$', password):
            e_data['error_info'] = '8-20字符的password'
            return render(request, 'common_error.html', e_data, status=403)
        if password2 != password:
            e_data['error_info'] = '密码不一致'
            return render(request, 'common_error.html', e_data, status=403)
        if not re.match(r"^\w+[-_.]*[a-zA-Z0-9_.+1]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$", email):
            e_data['error_info'] = '邮箱格式不符'
            return render(request, 'common_error.html', e_data, status=403)
        if allow != 'on':
            e_data['error_info'] = '未勾选xx协议'
            return render(request, 'common_error.html', e_data, status=403)

        redis_conn = get_redis_connection('verify_code')
        img_code_server = redis_conn.get(f'img_code_{uuid}')
        if not img_code_server:
            e_data['error_info'] = '图形验证码已过期'
            return render(request, 'common_error.html', e_data, status=403)
        if img_code_server.decode() != img_code:
            e_data['error_info'] = f'图形验证码不一致 {img_code_server.decode()} {img_code}'
            return render(request, 'common_error.html', e_data, status=403)

        sms_code_server = redis_conn.get(f'sms_code_{uuid}')
        if sms_code not in settings.__getattr__('FREE_SMS_CODE'):
            if not sms_code_server:
                e_data['error_info'] = '短信验证码已过期'
                return render(request, 'common_error.html', e_data, status=403)
            if sms_code_server.decode() != sms_code:
                e_data['error_info'] = f'短信验证码不一致'
                return render(request, 'common_error.html', e_data, status=403)

        try:
            new_user = User.objects.create_user(username=username, password=password, email=email)
        except DatabaseError as e:
            e_data['error_info'] = str(e)
            return render(request, 'common_error.html', e_data, status=403)

        login(request=request, user=new_user)

        response = redirect('/')
        cookie_expire = settings.__getattr__('COOKIE_EXPIRE') or 3600 * 24 * 7
        response.set_cookie(key='username', value=new_user.username, max_age=cookie_expire)
        return response


def index(request):
    user = request.user
    counts = User.objects.count()

    # upload = request.FILES.get('img')
    # if upload:
    #     user.img = upload
    #     user.save()

    data = {'counts': counts}

    if user.is_authenticated:
        data.update({
            'username': user.username,
            'email': user.email,
            'img': user.img,
            'atime': user.last_login,
            'ip': user.login_ip,
        })

    return render(request, 'index.html', data)


class LogoutPage(View):

    def get(self, request):
        _next = request.GET.get('next')
        logout(request)
        response = redirect(_next or '/')
        response.delete_cookie(key='username')
        return response


class ProfilePage(View):

    def get(self, request):

        return render(request, 'account/profile.html')


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
        # ip = get_ip.get_ip(request)
        temp = str(random.randint(1, 100000)) + random.choice(username) + random.choice(username)
        u.reset_password_salt = hmac.new(key=bytes(temp, encoding='utf-8'),
                                         msg=bytes(str(username+datetime.datetime.now()), encoding='utf-8'),
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
        sendmail.sendresetpassword(message=msg, to=email)

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
    else:
        return JsonResponse({'status': 401, 'msg': 'Unauthorized'}, status=401)


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


def drawcards(request):
    draw = draw_cards_arknight.Draw()
    try:
        no6 = request.session['no6']
        no5 = request.session['no5']
    except Exception as e:
        print(e)
        no6 = 0
        no5 = 0
    draw.count_no_5 = no5
    draw.count_no_6 = no6

    res = draw.draw10()
    request.session['no6'] = draw.count_no_6
    request.session['no5'] = draw.count_no_5
    res = [[x.name, x.stars, None] for x in res]
    for i in res:
        if i[1] == 6:
            i[1] = '#fff'
            i[2] = '#dc3545'
        elif i[1] == 5:
            i[1] = '#212529'
            i[2] = '#ffc107'
        elif i[1] == 4:
            i[1] = '#fff'
            i[2] = '#117a8b'
        elif i[1] == 3:
            i[1] = '#fff'
            i[2] = '#1e7e34'
        else:
            i[1] = '#212529'
            i[2] = '#dae0e5'
    # res = [(x.name, x.stars) for x in res]

    result = {
        'res': res,
        'no6': draw.count_no_6,
        'no5': draw.count_no_5,
    }
    # return HttpResponse(JsonResponse({'result': res}))
    return render(request, r'drawcards.html', result)


def reset_record(request):
    request.session['no6'] = 0
    request.session['no5'] = 0
    return render(request, r'drawcards.html', {'no6': 0, 'no5': 0})
