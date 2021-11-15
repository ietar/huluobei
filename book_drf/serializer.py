# -*- coding: utf-8 -*-
from rest_framework import serializers
from crawlers.models import Comment


class BookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    book_name = serializers.CharField()
    author = serializers.CharField()
    digest = serializers.CharField()
    read_count = serializers.IntegerField()
    collect_count = serializers.IntegerField()


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'


class CommentSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(required=False)
    chapter_count = serializers.IntegerField(required=False)
    user_name = serializers.CharField(allow_null=True, required=False)
    comment = serializers.CharField(required=False)
    ts = serializers.DateTimeField(allow_null=True, required=False)
    agree = serializers.IntegerField(allow_null=True, required=False)

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.book_id = validated_data.get('book_id', instance.book_id)
        instance.chapter_count = validated_data.get('chapter_count', instance.chapter_count)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance

