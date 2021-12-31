# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.any import ip2int, get_client_ip


class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request=request, user=user)
            user.login_ip = ip2int(get_client_ip(request))
            user.save()
        print(123)
        return Response('ok')
