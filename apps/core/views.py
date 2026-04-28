from django.http import JsonResponse
from django.shortcuts import render
from apps.packages.models import Package
from apps.categories.models import Category
from django.db.models import Count, Q
from .models import HeroImage


def health_check(request):
    return JsonResponse({"status": "ok"})


def home(request):
    # Categories with package count
    categories = list(
        Category.objects.annotate(
            active_package_count=Count("packages", filter=Q(packages__is_active=True))
        )
    )

    # Build a category_id → first package image URL mapping (one query)
    pkg_images = {}
    for pkg in (
        Package.objects.filter(is_active=True)
        .exclude(image="")
        .exclude(image__isnull=True)
        .select_related("category")
        .order_by("category_id", "-created_at")
    ):
        if pkg.category_id not in pkg_images:
            pkg_images[pkg.category_id] = pkg.image.url

    # Attach a resolved display_image URL to each category
    for cat in categories:
        if cat.image:
            cat.display_image = cat.image.url
        else:
            cat.display_image = pkg_images.get(cat.id)

    # Featured packages (homepage cards)
    featured_packages = Package.objects.select_related("category").filter(
        is_active=True
    )[:6]

    # Hero slides managed by admin
    hero_slides = list(
        HeroImage.objects.filter(is_active=True)
        .exclude(image="")
        .exclude(image__isnull=True)
        .order_by("order", "-created_at")
    )

    return render(
        request,
        "core/home.html",
        {
            "categories": categories,
            "featured_packages": featured_packages,
            "hero_slides": hero_slides,
        },
    )
