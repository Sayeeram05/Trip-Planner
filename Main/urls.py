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

# Serve local media files in development when cloud media is disabled
if settings.DEBUG and not settings.USE_CLOUDFLARE_R2:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
