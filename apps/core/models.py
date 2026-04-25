from django.db import models


class HeroImage(models.Model):
    image = models.ImageField(
        upload_to="hero/",
        help_text="Recommended: landscape image, at least 1920x1080 px",
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional caption displayed as alt text (not shown on slide)",
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first in the carousel",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Hero Image"
        verbose_name_plural = "Hero Images"

    def __str__(self):
        return self.title or f"Hero Image #{self.pk}"
