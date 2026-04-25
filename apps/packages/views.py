from django.shortcuts import render, get_object_or_404
from .models import Package
from apps.categories.models import Category
from django.db.models import Count, Q


def package_list(request):
    packages = Package.objects.select_related("category").filter(is_active=True)
    categories = Category.objects.annotate(
        active_package_count=Count("packages", filter=Q(packages__is_active=True))
    ).filter(active_package_count__gt=0)
    selected_category = None
    invalid_category = False

    category_id = request.GET.get("category")
    if category_id:
        try:
            selected_category = categories.get(id=category_id)
            packages = packages.filter(category=selected_category)
        except (Category.DoesNotExist, ValueError, TypeError):
            # Invalid category IDs should not 404; show a guided empty state instead.
            invalid_category = True
            packages = packages.none()

    return render(
        request,
        "packages/list.html",
        {
            "packages": packages,
            "categories": categories,
            "selected_category": selected_category,
            "invalid_category": invalid_category,
        },
    )


def package_detail(request, pk):
    package = get_object_or_404(
        Package.objects.prefetch_related("gallery", "itineraries"),
        id=pk,
        is_active=True,
    )
    itineraries = package.itineraries.all()
    gallery = package.gallery.all()
    return render(
        request,
        "packages/detail.html",
        {
            "package": package,
            "itineraries": itineraries,
            "gallery": gallery,
        },
    )
