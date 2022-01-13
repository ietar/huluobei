# from django.conf.urls.static import static
from django.urls import re_path
from rest_framework.routers import DefaultRouter

from . import views, account_views, crawl_views
# from huluobei import settings

urlpatterns = [
    re_path(r'^user_collections$', views.user_collections),
    re_path(r'^(?P<book_id>\d+)/(?P<chapter_count>\d+)$', views.UserCollections.as_view()),
    re_path(r'comment/(?P<book_id>\d+)/(?P<chapter_count>\d+)$', views.CommentApi.as_view()),

    # re_path(r'login/$', views.LoginView.as_view()),
    re_path(r'anything/$', views.AnythingView.as_view(), name='anything'),
    re_path(r'user_exist/$', views.UserExistView.as_view(), name='user_exist'),
    re_path(r'user/$', views.UserView.as_view(), name='user'),
    re_path(r'reset_password/$', views.ResetPasswordView.as_view(), name='reset_password'),
    re_path(r'crawl/get_content/$', crawl_views.get_content_view, name='get_content'),
]

router = DefaultRouter()
router.register('books', views.BookView, basename='books')
router.register('book_content', views.BookContentView, basename='book_content')
router.register('comment', views.CommentView, basename='comment')

urlpatterns += router.urls
