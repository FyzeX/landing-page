from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('process/', views.ProcessPaymentView.as_view(), name='process'),
    path('telegram/webhook/', views.TelegramWebhookView.as_view(), name='telegram_webhook'),
    path('success/<uuid:order_id>/', views.PaymentSuccessView.as_view(), name='success'),
    path('cancel/<uuid:order_id>/', views.PaymentCancelView.as_view(), name='cancel'),
]