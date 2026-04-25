import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from .models import Enquiry, EmailTemplate


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "updated_at"]
    readonly_fields = ["name", "updated_at"]
    fields = ["name", "subject", "html_body", "updated_at"]

    def has_add_permission(self, request):
        # Templates are seeded via migration; prevent accidental duplicates
        return False

    def has_delete_permission(self, request, obj=None):
        return False


def export_enquiries_csv(modeladmin, request, queryset):
    """Export selected enquiries as a CSV file."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="enquiries.csv"'
    writer = csv.writer(response)
    writer.writerow(
        [
            "Full Name",
            "Phone",
            "Email",
            "Location",
            "Destination",
            "Travel Date",
            "People",
            "Package",
            "Received On",
        ]
    )
    for enq in queryset:
        writer.writerow(
            [
                enq.full_name,
                enq.phone,
                enq.email,
                enq.location,
                enq.destination,
                enq.travel_date,
                enq.people_count,
                enq.package or "",
                enq.created_at.strftime("%Y-%m-%d %H:%M"),
            ]
        )
    return response


export_enquiries_csv.short_description = "Export selected enquiries to CSV"


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "phone_link",
        "email_link",
        "destination",
        "travel_date",
        "people_count",
        "created_at",
    ]
    list_filter = ["travel_date", "created_at"]
    search_fields = ["full_name", "phone", "email", "destination", "location"]
    list_per_page = 25
    actions = [export_enquiries_csv]
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

    def phone_link(self, obj):
        return format_html('<a href="tel:{}">{}</a>', obj.phone, obj.phone)

    phone_link.short_description = "Phone"
    phone_link.admin_order_field = "phone"

    def email_link(self, obj):
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)

    email_link.short_description = "Email"
    email_link.admin_order_field = "email"

    def has_add_permission(self, request):
        return False
