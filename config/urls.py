"""
Root URL configuration.

Notice: django.contrib.admin is NOT included here. All CRUD interfaces are
custom views defined in placement/urls.py, as required by the assignment.
"""
from django.urls import path, include

urlpatterns = [
    path("", include("placement.urls")),
]
