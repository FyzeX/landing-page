from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('auth/', include('users.api_urls')),
    path('templates/', include('templates.api_urls')),
    path('orders/', include('orders.api_urls')),
    path('payments/', include('payments.api_urls')),
]