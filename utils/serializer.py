# -*- coding: utf-8 -*-
# from abc import ABC

from rest_framework import serializers

from account.models import User
from crawlers.models import Book, BookContent, Comment
from utils.any import int2ip, list_sub


class SimpleModelSerializer(serializers.ModelSerializer):
    """
    可在使用时自定义fields 默认为__all__ model必传
    serializer = CustomFieldModelSerializer(fields=(field1, field2,...))
    """
    def __init__(self, model, fields=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not fields:
            fields = []
        if not isinstance(fields, list):
            fields = list(fields)
        exclude = ['create_time', 'update_time']
        fields = list_sub(fields, exclude)
        self.Meta.fields = fields or '__all__'
        self.Meta.model = model

    class Meta:
        pass


class UserSerializer(serializers.ModelSerializer):
    """
    login_ip fixed readonly
    """

    password = serializers.CharField(write_only=True)  # 密码不读
    login_ip = serializers.SerializerMethodField()

    def get_login_ip(self, obj):
        before = obj.login_ip
        after = int2ip(before)
        return after

    class Meta:
        model = User
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'
        # fields = ('book_id', 'book_name', 'author', 'digest', 'current', 'read_count', 'collect_count', 'using')


class BookContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookContent
        fields = '__all__'
        # fields = ('book_name', 'chapter_count', 'chapter', 'content', 'collect_count', 'read_count', 'using')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ('book_id', 'chapter_count', 'user_name', 'comment', 'ts', 'agree')
