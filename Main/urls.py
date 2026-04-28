"""
URL configuration for Sri Narpavi Holidays project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Admin site branding
admin.site.site_header = "SriNarpavi Holidays"
admin.site.site_title = "SriNarpavi Admin"
admin.site.index_title = "Welcome to SriNarpavi Holidays Portal"

urlpatterns = [
    path("snh-portal/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("categories/", include("apps.categories.urls")),
    path("packages/", include("apps.packages.urls")),
    path("enquiry/", include("apps.enquiries.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
