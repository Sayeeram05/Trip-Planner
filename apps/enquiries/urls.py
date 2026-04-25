from django.urls import path
from . import views

app_name = "enquiries"

urlpatterns = [
    path("new/<int:package_id>/", views.enquiry_create, name="create"),
    path("success/", views.enquiry_success, name="success"),
]
