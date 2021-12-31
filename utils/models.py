# -*- coding: utf-8 -*-
from django.db import models
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from utils.default_data import n_data


class BaseModel(models.Model):
    """为模型类 补充通用 字段"""
    objects = models.Manager()
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建数据的时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新数据的时间")

    class Meta:
        abstract = True


class CustomResponseModelViewSet(ModelViewSet):
    """
    对响应格式做微调
    """

    def create(self, request, *args, **kwargs):
        res = n_data()
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            res['result'] = False
            res['data'] = serializer.errors
            return Response(res, status=400)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        res['data'] = serializer.data
        return Response(serializer.data, status=201, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        res = n_data()
        res['data'] = serializer.data
        return Response(res)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        res = n_data()
        res['data'] = serializer.data
        return Response(res)

    def update(self, request, *args, **kwargs):
        res = n_data()
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid(raise_exception=False):
            res['result'] = False
            res['data'] = serializer.errors
            return Response(res, status=400)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        res['data'] = serializer.data
        return Response(res)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        res = n_data()
        return Response(data=res, status=204)
