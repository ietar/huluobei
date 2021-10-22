"""huluobei URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import RedirectView

from account import views
from huluobei import settings
from crawlers import urls as crawler_urls

urlpatterns = [
    re_path('^$', views.index),
    path('admin/', admin.site.urls),
    re_path('account/', include('account.urls')),
    re_path('api/', include('api.urls')),
    re_path('ajax_test/$', views.ajax_test),
    re_path('index/$', views.index),
    re_path('shit/$', views.shit),
    re_path('usercheck', views.usercheck),
    re_path('emailcheck', views.emailcheck),
    # re_path(r'^favicon.ico/$', serve, {'path': 'img/favicon.ico'}),  # 抄的 实现方式未知
    re_path(r'^drawcards/$', views.drawcards),
    re_path(r'^reset_record/$', views.reset_record),
    url(r'favicon.ico', RedirectView.as_view(url=r'static/img/favicon.ico')),
] + crawler_urls.urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
