from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^postData/$', views.postData, name='postData'),
    url(r'^raspberry/list/$', views.RaspberryListView.as_view(), name='raspberry-list'),
]
