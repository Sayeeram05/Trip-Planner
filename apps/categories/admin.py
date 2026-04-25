from django.contrib import admin
from django.utils.html import format_html
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["image_preview", "name", "created_at"]
    list_display_links = ["image_preview", "name"]
    search_fields = ["name", "description"]
    ordering = ["name"]
    list_per_page = 20
    readonly_fields = ["created_at", "image_preview"]
    fields = ["name", "description", "image", "image_preview", "created_at"]

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" alt="{}" style="width:110px;height:72px;object-fit:cover;border-radius:8px;border:1px solid #ddd;" />',
                obj.image.url,
                obj.name,
            )
        return "No image"

    image_preview.short_description = "Preview"
