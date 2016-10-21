from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^senadores/$', views.senadores, name='senadores'),
    url(r'^pecs$', views.pecs, name='pecs'),
]
