from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
# Create your views here.
from personal.models import User


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
        if password != User.objects.get(username__exact=username).password:
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
        newuser.password = password
        newuser.email = email
        newuser.save()
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
    # username = request.POST.get('askname')
    # u = User.objects.filter(username__exact=username)
    # data = {}
    # if username:
    #     data['asked'] = 'yes'
    # if u:
    #     data['username'] = u[0].username
    #     data['email'] = u[0].email
    data = {
        'asked': 'yes',
        'username': 'hard_coding_username',
        'email': 'fucking_shit',
    }
    return HttpResponse(JsonResponse(data))
