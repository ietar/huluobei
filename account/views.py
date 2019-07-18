import datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from account.models import User
import hmac
import random
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
    print(request.session)
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
    u = User.objects.get(username__exact=user['username'])

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
    return redirect(r'/account/index/')


def index1(request):
    username = request.POST.get('askname')
    u = User.objects.filter(username__exact=username)
    data = {}
    if username:
        data['asked'] = 'yes'
    if u:
        data['username'] = u[0].username
        data['email'] = u[0].email
    return render(request, 'index1.html', data)


def shit(request):
    username = request.POST.get('askname')
    u = User.objects.filter(username__exact=username)
    data = {}
    if username:
        data['asked'] = 'yes'
    if u:
        data['username'] = u[0].username
        data['email'] = u[0].email
    else:
        data['username'] = '查无此人'
        data['email'] = '邮箱当然也查不到'
    return HttpResponse(JsonResponse(data))


def usercheck(request):
    # print('usercheck called')
    username = request.POST.get('username')
    # print('username = ', username)
    u = User.objects.filter(username__exact=username)
    u = len(u)
    # print(u)
    return HttpResponse(JsonResponse({'username': u}))
