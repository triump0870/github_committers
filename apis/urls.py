from django.conf.urls import include, url
from apis.views import ListCommittee

urlpatterns = [
    url(r'^lists/$', ListCommittee.as_view(), name="list-toppers"),
]
