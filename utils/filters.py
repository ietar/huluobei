# -*- coding: utf-8 -*-
from django_filters import FilterSet

from account.models import User as User_model
from crawlers.models import Book, BookContent, Comment


class UserFilter(FilterSet):
    class Meta:
        model = User_model
        fields = {
            'username': ['exact', 'icontains'],
            'id': ['exact', 'lt', 'gt']
        }


class BookFilter(FilterSet):
    class Meta:
        model = Book
        fields = {
            # 'book_name': ['exact', 'icontains'],
            'book_name': ['exact'],
            'author': ['exact', 'icontains'],
            'using': ['exact'],
            'book_id': ['exact', 'lt', 'gt']
        }


class BookContentFilter(FilterSet):
    class Meta:
        model = BookContent
        fields = {
            # 'book_name': ['exact', 'icontains'],
            'book_name': ['exact'],
            'chapter': ['exact', 'icontains'],
            'chapter_count': ['exact', 'lt', 'gt']
        }


class CommentFilter(FilterSet):
    class Meta:
        model = Comment
        fields = {
            'book_id': ['exact'],
            'comment': ['icontains'],
            'agree': ['exact', 'lt', 'gt']
        }