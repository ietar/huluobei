# -*- coding: utf-8 -*-
# from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
# from django.shortcuts import render
# from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

from crawlers.models import Book as Book_model
from book_drf.serializer import BookSerializer


# Create your views here.
class Books(APIView):
    def get_res(self):
        temp = {'result': False, 'data': None, 'msg': ''}
        return dict(**temp)

    def get(self, request):
        print(request.data, request.query_params)
        books = Book_model.objects.all()
        # c1 = BookContent.objects.get(id=1)
        # print(c1.book_name.book_name)

        # 关联查询 主表对象.(foreign_model.lower())_set
        # book1 = Book_model.objects.get(book_id=1)
        # contents = BookContent.objects.filter(book_name_id=book_id)
        # contents = book1.bookcontent_set.all()
        # print(contents)

        ser = BookSerializer(books, many=True)
        res = self.get_res()
        res['data'] = ser.data

        # return JsonResponse(ser.data, safe=False, json_dumps_params={
        #     'ensure_ascii': False})
        return Response(data=res)


class Book(APIView):
    def get_res(self):
        temp = {'result': False, 'data': None, 'msg': ''}
        return dict(**temp)

    def get(self, request, book_id):
        print(request.data, request.query_params)
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

        # return JsonResponse(res, json_dumps_params={
        #     'ensure_ascii': False})
        return Response(data=res)
