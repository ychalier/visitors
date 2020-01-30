from django.urls import path
from django.conf.urls import url
from . import views

app_name = "visitors"

urlpatterns = [
    # url("^dummy.*", views.dummy, name="dummy"),
    path("monitor", views.monitor, name="monitor"),
    path("api", views.api, name="api"),
    path("dump", views.dump, name="dump"),
]
