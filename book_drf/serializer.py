# -*- coding: utf-8 -*-
from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    book_name = serializers.CharField()
    author = serializers.CharField()
    digest = serializers.CharField()
    read_count = serializers.IntegerField()
    collect_count = serializers.IntegerField()
