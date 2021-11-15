# -*- coding: utf-8 -*-
# from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
# from django.shortcuts import render
# from django.views import View
# from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from django.http import JsonResponse
from django.http.request import QueryDict
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from crawlers.models import Book as Book_model, Comment as Comment_model
from book_drf.serializer import BookSerializer, CommentSerializer


# Create your views here.
class Books(GenericAPIView):

    queryset = Book_model.objects.all()
    serializer_class = BookSerializer

    def get_res(self):
        temp = {'result': False, 'data': None, 'msg': ''}
        return dict(**temp)

    def get(self, request):
        # print(request.data, request.query_params)
        # books = Book_model.objects.all()
        books = self.get_queryset()

        # c1 = BookContent.objects.get(id=1)
        # print(c1.book_name.book_name)

        # 关联查询 主表对象.(foreign_model.lower())_set
        # book1 = Book_model.objects.get(book_id=1)
        # contents = BookContent.objects.filter(book_name_id=book_id)
        # contents = book1.bookcontent_set.all()
        # print(contents)

        ser = self.get_serializer(books, many=True)
        # ser = BookSerializer(books, many=True)
        res = self.get_res()
        res['data'] = ser.data
        res['result'] = True

        # return JsonResponse(ser.data, safe=False, json_dumps_params={
        #     'ensure_ascii': False})
        return Response(data=res)


# class Book(GenericAPIView):
#     queryset = Book_model.objects.all()
#     serializer_class = BookSerializer
#
#     def get_res(self):
#         temp = {'result': False, 'data': None, 'msg': ''}
#         return dict(**temp)
#
#     def get(self, request, book_id):
#         print(request.data, request.query_params)
#         res = self.get_res()
#         try:
#             book1 = Book_model.objects.get(book_id=book_id)
#             print('121:', book_id, book1)
#             # books = self.get_queryset()
#
#             ser = BookSerializer(book1, many=False)
#             # ser.is_valid()
#
#             res['result'] = True
#             res['data'] = ser.data
#
#         except Book_model.DoesNotExist:
#             res['msg'] = 'not found'
#             return JsonResponse(res, json_dumps_params={
#                 'ensure_ascii': False}, status=404)
#
#         # return JsonResponse(res, json_dumps_params={
#         #     'ensure_ascii': False})
#         return Response(data=res)

class Book(ModelViewSet):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    queryset = Book_model.objects.all()
    serializer_class = BookSerializer


class Comment(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Comment_model.objects.all()
    serializer_class = CommentSerializer

    def get(self, request):
        return self.list(request)
        # comments = self.get_queryset().filter(book_id=book_id, chapter_count=chapter_count)
        # ser = self.get_serializer(comments, many=True)
        # return Response(data=ser.data)

    # def post(self, request: QueryDict, book_id, chapter_count):
    def post(self, request: QueryDict):
        try:
            return self.create(request)
        except Exception as e:
            import traceback
            traceback.print_exc()
            # print(e)
            return Response({'msg': str(e)}, 400)
        # c = self.get_object()
        # print('c=', c)

        data = request.data
        print(data, type(data))
        temp = {'book_id': book_id, 'chapter_count': chapter_count}
        temp.update(data)
        print('temp:', temp)

        # new_comment = Comment_model.objects.create()
        ser = self.get_serializer(data=temp)
        if ser.is_valid():
            ser.save()
            return Response(data=ser.data)
        else:
            # ser.save()
            res = {'msg': 'invalid',
                   'data': ser.errors}
            return Response(data=res, status=400)



