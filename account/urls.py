from django.urls import re_path
from account import views

urlpatterns = [

    # re_path(r'resetpassword/$', views.resetpassword),
    re_path(r'sendresetmail/$', views.sendresetmail),
    re_path(r'reset/$', views.reset),
    re_path(r'reset_done/$', views.reset_done),
    # re_path(r'upload/$', views.upload),

    re_path(r'login/$', views.LoginPage.as_view(), name='login'),
    re_path(r'register/$', views.RegisterPage.as_view(), name='register'),
    re_path(r'logout/$', views.LogoutPage.as_view(), name='logout'),
    re_path(r'profile/$', views.ProfilePage.as_view(), name='profile'),
    re_path(r'reset_password/$', views.resetpassword, name='reset_password'),  # todo


]
