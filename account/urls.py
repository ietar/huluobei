from django.conf.urls.static import static
from django.urls import re_path
from account import views
from zhihu_django import settings

urlpatterns = [
    re_path(r'login/$', views.login),
    re_path(r'logined/$', views.logined),
    re_path(r'regist/$', views.regist),
    re_path(r'registed/$', views.registed),
    re_path(r'index/$', views.index),
    re_path(r'logout/$', views.logout),
    # re_path(r'upload/$', views.upload),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)