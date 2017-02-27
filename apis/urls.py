from django.conf.urls import include, url
from apis.views import Committers

urlpatterns = [
    url(r'^lists/$', Committers.as_view(), name="list-toppers"),
]
