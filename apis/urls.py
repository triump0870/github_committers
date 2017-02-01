from django.conf.urls import include, url
from apis.views import ListToppers

urlpatterns = [
    url(r'^lists/$', ListToppers.as_view(), name="list-toppers"),
]
