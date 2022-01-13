from django.urls import re_path
# from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    re_path(r'^$', views.BackGroundPage.as_view(), name='index'),
    re_path(r'^books/$', views.BookPage.as_view(), name='books'),
    re_path(r'^book_content/$', views.BookContentPage.as_view(), name='book_content'),
]

