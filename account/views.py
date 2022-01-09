import datetime
import hmac
import random
import re

from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django_redis import get_redis_connection
from rest_framework.views import APIView

from account.models import User
from ietar_py_scripts import sendmail, draw_cards_arknight
# Create your views here.
from utils.any import ip2int, get_client_ip, hidden_email
from utils.default_data import e_data


class LoginPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(to='/')
        return render(request, 'account/login.html')

    def post(self, request):
        error_data = {'error_info': '',
                      'return_page': '/login',
                      'return_text': '回登录页面'}

        dic = request.POST
        username = dic.get('username')
        password = dic.get('password')
        img_code = dic.get('img_code')
        uuid = dic.get('uuid')

        if not all((username, password, img_code, uuid)):
            error_data['error_info'] = f'param username: {username}, password: {password},' \
                f' img_code: {img_code}, uuid: {uuid} required'
            return render(request, 'common_error.html', error_data, status=403)

        redis_conn = get_redis_connection('verify_code')
        img_code_server = redis_conn.get(f'img_code_{uuid}')
        if not img_code_server:
            error_data['error_info'] = '图形验证码已过期'
            return render(request, 'common_error.html', error_data, status=403)
        if img_code_server.decode() != img_code:
            error_data['error_info'] = f'图形验证码不一致 {img_code_server.decode()} {img_code}'
            return render(request, 'common_error.html', error_data, status=403)

        user = authenticate(username=username, password=password)
        if user is None:
            error_data['error_info'] = f'authenticate failed'
            return render(request, 'common_error.html', error_data, status=403)
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
        error_data = e_data()
        error_data['return_page'] = '/register/'
        error_data['return_text'] = '回注册页面'

        username = dic.get('username')
        password = dic.get('password')
        password2 = dic.get('password2')
        email = dic.get('email')
        allow = dic.get('allow')
        uuid = dic.get('uuid')
        img_code = dic.get('img_code')
        sms_code = dic.get('sms_code')

        if not all((username, password, password2, email, allow, uuid, img_code)):
            error_data['error_info'] = 'param username, password, password2, mobile, allow, uuid, img_code required'
            return render(request, 'common_error.html', error_data, status=403)
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            error_data['error_info'] = '5-20字符的username'
            return render(request, 'common_error.html', error_data, status=403)
        if not re.match(r'^.{8,20}$', password):
            error_data['error_info'] = '8-20字符的password'
            return render(request, 'common_error.html', error_data, status=403)
        if password2 != password:
            error_data['error_info'] = '密码不一致'
            return render(request, 'common_error.html', error_data, status=403)
        if not re.match(r"^\w+[-_.]*[a-zA-Z0-9_.+1]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$", email):
            error_data['error_info'] = '邮箱格式不符'
            return render(request, 'common_error.html', error_data, status=403)
        if allow != 'on':
            error_data['error_info'] = '未勾选xx协议'
            return render(request, 'common_error.html', error_data, status=403)

        redis_conn = get_redis_connection('verify_code')
        img_code_server = redis_conn.get(f'img_code_{uuid}')
        if not img_code_server:
            error_data['error_info'] = '图形验证码已过期'
            return render(request, 'common_error.html', error_data, status=403)
        if img_code_server.decode() != img_code:
            error_data['error_info'] = f'图形验证码不一致 {img_code_server.decode()} {img_code}'
            return render(request, 'common_error.html', error_data, status=403)

        sms_code_server = redis_conn.get(f'sms_code_{uuid}')
        if sms_code not in settings.__getattr__('FREE_SMS_CODE'):
            if not sms_code_server:
                error_data['error_info'] = '短信验证码已过期'
                return render(request, 'common_error.html', error_data, status=403)
            if sms_code_server.decode() != sms_code:
                error_data['error_info'] = f'短信验证码不一致'
                return render(request, 'common_error.html', error_data, status=403)

        try:
            new_user = User.objects.create_user(username=username, password=password, email=email)
        except DatabaseError as e:
            error_data['error_info'] = str(e)
            return render(request, 'common_error.html', error_data, status=403)

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


# def ajax_test(request):
#     username = request.POST.get('askname')
#     u = User.objects.filter(username__exact=username)
#     data = {}
#     if username:
#         data['asked'] = 'yes'
#     if u:
#         data['username'] = u[0].username
#         data['email'] = u[0].email
#     return render(request, 'ajax_test.html', data)


# def shit(request):
#     username = request.POST.get('askname')
#     u = User.objects.filter(username__exact=username)
#     data = {}
#     if username:
#         data['asked'] = 'yes'
#     else:
#         return HttpResponse('这么访问不行啊')
#     if u:
#         data['username'] = u[0].username
#         data['email'] = u[0].email
#     else:
#         data['username'] = '查无此人'
#         data['email'] = '邮箱当然也查不到'
#     return HttpResponse(JsonResponse(data))


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


def forget_password(request):
    return render(request, r'account/forget_password.html')


class ForgetPasswordEmailView(APIView):
    def post(self, request):
        username = request.POST.get('username')
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            res = e_data()
            res['error_info'] = '不存在该用户'
            res['return_text'] = '回忘记密码页'
            res['return_page'] = '/account/forget_password/'
            return render(request, 'common_error.html', res)

        username = user.username
        uid = user.id
        email = user.email

        temp = str(random.randint(1, 100000)) + random.choice(username) + random.choice(username)
        user.reset_password_salt = hmac.new(key=bytes(temp, encoding='utf-8'),
                                            msg=bytes(username + str(timezone.now()), encoding='utf-8'),
                                            digestmod='MD5').hexdigest()
        temp = user.reset_password_salt
        user.reset_time = timezone.now()
        user.save()
        m_email = hidden_email(user.email)
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

    您只需在提交请求后的 {ttl} 分钟内，通过点击下面的链接重置您的密码：
    {url}
    (如果上面不是链接形式，请将该地址手工粘贴到浏览器地址栏再访问)
    在上面的链接所打开的页面中输入新的密码后提交，您即可使用新的密码登录网站了。您可以在用户控制面板中随时修改您的密码。

    本请求提交者的 IP 为 {ip}

    此致
    {host} 管理团队. {host}
    '''.format(username=user.username, host=request.get_host(), ip=ip,
               url=f'{request.scheme}://{request.get_host()}/account/reset?resetsalt={temp}&id={uid}',
               ttl=settings.__getattr__('RESET_PASSWORD_EMAIL_TTL_MINUTES'))
        sendmail.sendresetpassword(message=msg, to=email)

        return HttpResponse('已成功发送找回邮件至 {}'.format(m_email))


class ResetPasswordView(APIView):
    def get(self, request):
        data = {}
        res = e_data()
        reset_salt = request.GET.get('resetsalt')
        uid = request.GET.get('id')
        try:
            user = User.objects.get(id=uid, reset_password_salt__exact=reset_salt)
            data['username'] = user.username
            data['reset_password_salt'] = reset_salt

        except ObjectDoesNotExist:
            res['error_info'] = '不存在该用户 或 没有请求重置密码'
            return render(request, 'common_error.html', res)

        ttl = settings.__getattr__('RESET_PASSWORD_EMAIL_TTL_MINUTES')
        if not user.reset_time or user.reset_time + datetime.timedelta(minutes=ttl) < timezone.now():
            res['error_info'] = '重置密码链接过期'
            return render(request, 'common_error.html', res)

        return render(request, r'account/reset.html', data)


def reset_done(request):
    res = e_data()
    username = request.POST.get('username')
    password = request.POST.get('password')
    re_password = request.POST.get('re_password')
    reset_password_salt = request.POST.get('reset_password_salt')
    if password != re_password:
        res['error_info'] = '两次密码不一致'
        return render(request, 'common_error.html', res)
    try:
        user = User.objects.get(username=username, reset_password_salt=reset_password_salt)
    except ObjectDoesNotExist:
        res['error_info'] = '不存在该用户'
        return render(request, 'common_error.html', res)

    if not user.reset_time or user.reset_time + datetime.timedelta(minutes=3) < timezone.now():
        res['error_info'] = '链接过期'
        return render(request, 'common_error.html', res)

    user.set_password(password)
    user.reset_time = None
    user.reset_password_salt = None
    user.save()

    msg = {'msg': '重置密码成功'}
    return render(request, 'message.html', msg)


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
