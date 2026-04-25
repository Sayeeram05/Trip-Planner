from django.db import models
from apps.packages.models import Package


class EmailTemplate(models.Model):
    """
    Stores editable email templates for enquiry notifications.
    'name' is a fixed lookup key — do not change it after seeding.
    In subject/html_body you can use Django template variables, e.g.:
        {{ full_name }}, {{ email }}, {{ phone }}, {{ location }},
        {{ destination }}, {{ travel_date }}, {{ people_count }}, {{ package }}
    """

    ADMIN_NOTIFICATION = "admin_notification"
    CUSTOMER_CONFIRMATION = "customer_confirmation"

    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=300)
    html_body = models.TextField(
        help_text=(
            "HTML email body. Available variables: "
            "{{ full_name }}, {{ email }}, {{ phone }}, {{ location }}, "
            "{{ destination }}, {{ travel_date }}, {{ people_count }}, {{ package }}"
        )
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Email Template"
        verbose_name_plural = "Email Templates"

    def __str__(self):
        return self.name


class Enquiry(models.Model):
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    location = models.CharField(max_length=200)
    destination = models.CharField(max_length=300)
    travel_date = models.DateField()
    people_count = models.PositiveIntegerField()
    package = models.ForeignKey(
        Package, on_delete=models.SET_NULL, null=True, related_name="enquiries"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Enquiries"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} — {self.destination}"
