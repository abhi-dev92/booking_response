# xml_manager/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import XMLFileViewSet

# Create a router and register the ViewSet
router = DefaultRouter()
router.register(r'xmlfiles', XMLFileViewSet, basename='xmlfile')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
]
