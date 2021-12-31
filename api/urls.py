# from django.conf.urls.static import static
from django.urls import re_path
from . import views, account_views
# from huluobei import settings

urlpatterns = [
    re_path(r'^user_collections$', views.user_collections),
    re_path(r'^(?P<book_id>\d+)/(?P<chapter_count>\d+)$', views.UserCollections.as_view()),
    re_path(r'comment/(?P<book_id>\d+)/(?P<chapter_count>\d+)$', views.CommentApi.as_view()),

    # re_path(r'login/$', views.LoginView.as_view()),
    re_path(r'anything/$', views.AnythingView.as_view(), name='anything'),
    re_path(r'user_exist/$', views.UserExistView.as_view(), name='user_exist'),
    re_path(r'user/$', views.UserView.as_view(), name='user'),
]
