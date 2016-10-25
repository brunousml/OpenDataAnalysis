from . import views

from django.conf.urls import url, include
from tastypie.api import Api
from senate.tastypieResources import *


v1_api = Api(api_name='v1')
v1_api.register(ParliamentaryResource())
v1_api.register(StateResource())

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^parliamentarians/$', views.parliamentarians, name='parliamentarians'),
    url(r'^pecs$', views.pecs, name='pecs'),
    url(r'^api/', include(v1_api.urls))
]
