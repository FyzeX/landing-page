from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import TemplateViewSet, CategoryViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'templates', TemplateViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'reviews', ReviewViewSet, basename='review')

app_name = 'templates_api'

urlpatterns = [
    path('', include(router.urls)),
]