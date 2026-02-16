"""
Main URL configuration for the SaaS Financial Platform.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "SaaS Financial Platform Admin"
admin.site.site_title = "SaaS Financial Platform"
admin.site.index_title = "Administration"
