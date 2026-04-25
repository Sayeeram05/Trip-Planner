from django.contrib import admin
from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "phone",
        "email",
        "destination",
        "travel_date",
        "people_count",
        "created_at",
    ]
    list_filter = ["travel_date", "created_at"]
    search_fields = ["full_name", "phone", "email", "destination", "location"]
    readonly_fields = [
        "full_name",
        "phone",
        "email",
        "location",
        "destination",
        "travel_date",
        "people_count",
        "package",
        "created_at",
    ]
    ordering = ["-created_at"]

    def has_add_permission(self, request):
        return False
