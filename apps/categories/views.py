from django.shortcuts import render
from .models import Category
from django.db.models import Count, Q


def category_list(request):
    categories = Category.objects.annotate(
        active_package_count=Count("packages", filter=Q(packages__is_active=True))
    )
    return render(request, "categories/list.html", {"categories": categories})
