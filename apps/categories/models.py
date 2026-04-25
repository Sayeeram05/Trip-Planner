from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="categories/",
        null=True,
        blank=True,
        help_text="Optional category cover image (WebP preferred) shown on homepage cards",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name
