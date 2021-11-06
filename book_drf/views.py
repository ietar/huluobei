# -*- coding: utf-8 -*-
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from crawlers.models import Book as Book_model
from book_drf.serializer import BookSerializer


# Create your views here.
class Books(View):
    def get_res(self):
        temp = {'result': False, 'data': None, 'msg': ''}
        return dict(**temp)

    def get(self, request):
        books = Book_model.objects.all()
        print(books)
        ser = BookSerializer(books, many=True)
        return JsonResponse(ser.data, safe=False, json_dumps_params={
            'ensure_ascii': False})


class Book(View):
    def get_res(self):
        temp = {'result': False, 'data': None, 'msg': ''}
        return dict(**temp)

    def get(self, request, book_id):
        res = self.get_res()
        try:
            book1 = Book_model.objects.get(book_id=book_id)

            ser = BookSerializer(book1, many=False)
            res['result'] = True
            res['data'] = ser.data

        except Book_model.DoesNotExist:
            res['msg'] = 'not found'
            return JsonResponse(res, json_dumps_params={
                'ensure_ascii': False}, status=404)

        return JsonResponse(res, json_dumps_params={
            'ensure_ascii': False})
