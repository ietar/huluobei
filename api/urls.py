# from django.conf.urls.static import static
from django.urls import re_path
from api import views
# from huluobei import settings

urlpatterns = [
    re_path(r'^user_collections$', views.user_collections),
    re_path(r'^(?P<book_id>\d+)/(?P<chapter_count>\d+)$', views.UserCollections.as_view()),
    re_path(r'comment/(?P<book_id>\d+)/(?P<chapter_count>\d+)$', views.CommentApi.as_view()),
]
