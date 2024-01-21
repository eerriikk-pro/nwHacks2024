"""
URL configuration for nwhacks2024 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import load_map, process_place_id, process_image, menu_gallery, menu_filter

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", load_map, name="load_map"),
    path("processing/", process_place_id, name='process_place_id'),
    path("menu_gallery/", menu_gallery, name="menu_gallery"),
    path("process-image/", process_image, name="process_image"),
    path("menu_filter/", menu_filter, name="menu_filter")
]
