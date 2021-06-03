# myapp/urls.py
from django.conf.urls import url
from django.urls import path, re_path
from .views import home, search_page, repeat

app_name = 'searchpage'

urlpatterns = [

    re_path(r'page/$',repeat,name="page"),
    re_path(r'search/$', search_page, name="search"),
    path('', home, name="homepage"),
]