from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^parliamentarians/$', views.parliamentarians, name='parliamentarians'),
    url(r'^pecs$', views.pecs, name='pecs'),
]
