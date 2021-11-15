from django.conf.urls.static import static
from django.urls import re_path
from . import views, views1, views2
from huluobei import settings

urlpatterns = [
    # re_path(r'^books/', views.Books.as_view()),
    # re_path(r'^book/(?P<book_id>\d+)/$', views.Book.as_view()),

    # re_path(r'^books/', views1.Books.as_view()),
    # re_path(r'^books/(?P<book_id>\d+)/$', views1.Book.as_view()),

    re_path(r'^books/$', views2.Books.as_view()),
    # re_path(r'^books/(?P<book_id>\d+)/$', views2.Book.as_view()),
    re_path(r'^books/(?P<pk>\d+)/$', views2.Book.as_view({'get': 'retrieve', 'post': 'create'})),
    # re_path(r'^comment/(?P<book_id>\d+)/(?P<chapter_count>\d+)/$', views2.Comment.as_view())
    re_path(r'^comment/$', views2.Comment.as_view())
]
