from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from utils.default_data import e_data


class BackGroundPage(View):

    def get(self, request):
        return redirect(reverse('background:books'))


class BookPage(View):
    def get(self, request):
        user = request.user
        if user.is_staff or user.is_superuser:
            return render(request, 'background/books.html')
        else:
            error_data = e_data()
            error_data['error_info'] = '非管理员无法访问'
            return render(request, 'common_error.html', error_data, status=401)


class BookContentPage(View):
    def get(self, request):
        user = request.user
        if user.is_staff or user.is_superuser:
            return render(request, 'background/book_content.html')
        else:
            error_data = e_data()
            error_data['error_info'] = '非管理员无法访问'
            return render(request, 'common_error.html', error_data, status=401)
