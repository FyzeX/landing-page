from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

app_name = 'orders_api'

urlpatterns = [
    path('', include(router.urls)),
]