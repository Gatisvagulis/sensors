"""
URL configuration for sensor project.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/", include("polls.urls")),
    path("admin/", admin.site.urls),
]
