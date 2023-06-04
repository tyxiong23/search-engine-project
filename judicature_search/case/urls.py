from django.urls import include, path
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import *  # Make sure both views are imported

router = DefaultRouter()
router.register(r'cases', CaseViewSet, basename='case')

urlpatterns = [
    path('search/', search_view, name='search'),  # The search view is at /case/search/
    path('', include(router.urls)),  # The router's urls are included at /case/
]
