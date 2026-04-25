from django.db import models
from apps.packages.models import Package


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
