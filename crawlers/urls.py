from django.conf.urls.static import static
from django.urls import re_path
from crawlers import views
from zhihu_django import settings

urlpatterns = [
    re_path(r'book/get_chapter', views.get_chapter),
    re_path(r'book/get_content', views.get_content)
]
