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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path, include
from django.views.generic import RedirectView

from account import views
from django.conf import settings
from verifications import views as verification_view

urlpatterns = [
    re_path('^$', views.index),
    path('admin/', admin.site.urls),
    re_path('^', include(('account.urls', 'account'), namespace='account')),
    re_path('^api/', include('api.urls')),
    re_path('^', include('crawlers.urls')),
    re_path('^book_drf/', include('book_drf.urls')),
    re_path('^background/', include(('background.urls', 'background'), namespace='background')),

    # re_path('ajax_test/$', views.ajax_test),
    re_path('^index/$', views.index),
    # re_path('shit/$', views.shit),
    re_path('usercheck', views.usercheck),
    re_path('emailcheck', views.emailcheck),
    # re_path(r'^favicon.ico/$', serve, {'path': 'img/favicon.ico'}),  # 抄的 实现方式未知
    re_path(r'^drawcards/$', views.drawcards),
    re_path(r'^reset_record/$', views.reset_record),

    re_path(r'^image_codes/(?P<uuid>[\w-]+)/$', verification_view.ImageCodeView.as_view(), name='image_codes'),
    url(r'favicon.ico', RedirectView.as_view(url=r'static/img/favicon.ico')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
