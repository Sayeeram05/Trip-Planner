from django.contrib import admin
from django.utils.html import format_html

from .models import HeroImage


def activate_hero_images(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(request, f"{updated} hero image(s) activated.")


def deactivate_hero_images(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(request, f"{updated} hero image(s) deactivated.")


activate_hero_images.short_description = "Activate selected hero images"
deactivate_hero_images.short_description = "Deactivate selected hero images"


@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = [
        "image_preview",
        "title",
        "order",
        "is_active",
        "created_at",
    ]
    list_display_links = ["image_preview", "title"]
    list_editable = ["order", "is_active"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["title"]
    ordering = ["order", "-created_at"]
    list_per_page = 20
    save_on_top = True
    actions = [activate_hero_images, deactivate_hero_images]
    readonly_fields = ["created_at", "image_preview"]
    fields = ["image", "image_preview", "title", "is_active", "order", "created_at"]

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" alt="{}" style="width:120px;height:72px;object-fit:cover;border-radius:8px;border:1px solid #ddd;" />',
                obj.image.url,
                obj.title or "Hero image",
            )
        return "No image"

    image_preview.short_description = "Preview"
