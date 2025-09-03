from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='list'),
    path('<uuid:pk>/', views.OrderDetailView.as_view(), name='detail'),
    path('create/', views.CreateOrderView.as_view(), name='create'),
    path('download/<str:token>/', views.DownloadTemplateView.as_view(), name='download'),
]