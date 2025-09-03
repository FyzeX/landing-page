from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('api/', include(router.urls)),
]