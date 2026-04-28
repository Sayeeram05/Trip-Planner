from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("healthz/", views.health_check, name="health_check"),
    path("", views.home, name="home"),
]
