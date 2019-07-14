from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
# Create your views here.
from personal.models import User
import hmac
import random


def login(request):
    return render(request, 'personal/login.html')


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
    return render(request, 'personal/logined.html', data)


def regist(request):
    data = {

    }
    return render(request, 'personal/regist.html', data)


def registed(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    result = 'ok'
    user = User.objects.filter(username__exact=username)
    print(len(user))
    if len(user) >= 1:
        result = 'not ok'
    else:
        newuser = User()
        newuser.username = username
        newuser.salt = str(random.randint(1, 100000)) + random.choice(username) + random.choice(username)
        newuser.password = hmac.new(key=bytes(newuser.salt, encoding='utf-8'), msg=bytes(password, encoding='utf-8'),
                                    digestmod='MD5').hexdigest()
        newuser.email = email
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
    return render(request, 'personal/registed.html', data)


def index(request):
    try:
        user = request.session['user']
    except KeyError:
        data = {

        }
        return render(request, 'personal/index.html', data)
    u = User.objects.get(username__exact=user['username'])
    upload = request.FILES.get('img')
    if upload:
        u.img = upload
        u.save()
    data = {
        'username': user['username'],
        'email': user['email'],
        'img': u.img,
    }
    # print(user)
    # print(upload)
    return render(request, 'personal/index.html', data)


def logout(request):
    request.session.clear()
    return render(request, 'personal/index.html')


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
