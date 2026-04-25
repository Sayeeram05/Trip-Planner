from django.db import models
from apps.categories.models import Category


class Package(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="packages"
    )
    title = models.CharField(max_length=300)
    description = models.TextField()
    duration = models.CharField(max_length=100, help_text="e.g. 5 Days / 4 Nights")
    group_size = models.CharField(max_length=100, help_text="e.g. 2–10 People")
    language = models.CharField(max_length=100, help_text="e.g. English, Tamil")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Per person price in INR (leave blank if on request)",
    )
    image = models.ImageField(
        upload_to="packages/",
        null=True,
        blank=True,
        help_text="Package cover image (WebP preferred)",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class PackageImage(models.Model):
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name="gallery"
    )
    image = models.ImageField(
        upload_to="packages/gallery/",
        help_text="Additional package image (WebP preferred)",
    )
    caption = models.CharField(max_length=200, blank=True, help_text="Optional caption")
    order = models.PositiveIntegerField(
        default=0, help_text="Display order (lower = first)"
    )

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Image {self.order} — {self.package.title}"


class Itinerary(models.Model):
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name="itineraries"
    )
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=300)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["day_number"]
        verbose_name_plural = "Itineraries"

    def __str__(self):
        return f"Day {self.day_number}: {self.title}"
