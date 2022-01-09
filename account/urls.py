from django.urls import re_path

from account import views

urlpatterns = [

    # re_path(r'resetpassword/$', views.resetpassword),
    # re_path(r'sendresetmail/$', views.sendresetmail, name='send_reset_email'),
    # re_path(r'reset/$', views.reset),
    # re_path(r'reset_done/$', views.reset_done),
    # re_path(r'upload/$', views.upload),

    re_path(r'login/$', views.LoginPage.as_view(), name='login'),
    re_path(r'register/$', views.RegisterPage.as_view(), name='register'),
    re_path(r'logout/$', views.LogoutPage.as_view(), name='logout'),
    re_path(r'profile/$', views.ProfilePage.as_view(), name='profile'),
    re_path(r'^account/forget_password/$', views.forget_password, name='forget_password'),
    re_path(r'^account/send_reset_email/$', views.ForgetPasswordEmailView.as_view(), name='send_reset_email'),
    re_path(r'^account/reset/$', views.ResetPasswordView.as_view()),
    re_path(r'^account/reset_done/$', views.reset_done),
]
