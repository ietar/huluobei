from django.conf.urls.static import static
from django.urls import re_path
from . import views
from huluobei import settings

urlpatterns = [
    re_path(r'^books/', views.Books.as_view()),
    re_path(r'^book/(?P<book_id>\d+)/$', views.Book.as_view()),
]
