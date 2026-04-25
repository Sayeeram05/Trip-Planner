from django.contrib import admin
from django.utils.html import format_html

from .models import Itinerary, Package, PackageImage


class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 2
    fields = ["day_number", "title", "description"]
    ordering = ["day_number"]


class PackageImageInline(admin.TabularInline):
    model = PackageImage
    extra = 3
    fields = ["image_preview", "image", "caption", "order"]
    readonly_fields = ["image_preview"]
    ordering = ["order"]

    def image_preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" alt="preview" style="width:90px;height:60px;object-fit:cover;border-radius:6px;border:1px solid #ddd;" />',
                obj.image.url,
            )
        return "—"

    image_preview.short_description = "Preview"


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    inlines = [PackageImageInline, ItineraryInline]
    list_display = [
        "image_preview",
        "title",
        "category",
        "duration",
        "price",
        "is_active",
        "created_at",
    ]
    list_display_links = ["image_preview", "title"]
    list_filter = ["category", "is_active", "created_at"]
    search_fields = ["title", "description"]
    list_editable = ["is_active"]
    readonly_fields = ["created_at", "image_preview"]
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("category", "title", "description", "image", "image_preview")},
        ),
        (
            "Package Details",
            {"fields": ("duration", "group_size", "language", "price")},
        ),
        ("Status", {"fields": ("is_active", "created_at")}),
    )

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" alt="{}" style="width:110px;height:72px;object-fit:cover;border-radius:8px;border:1px solid #ddd;" />',
                obj.image.url,
                obj.title,
            )
        return "No image"

    image_preview.short_description = "Preview"


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ["package", "day_number", "title", "created_at"]
    list_filter = ["package"]
    search_fields = ["title", "description"]
    ordering = ["package", "day_number"]
