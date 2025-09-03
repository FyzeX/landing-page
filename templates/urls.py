from django.urls import path
from . import views

app_name = 'templates'

urlpatterns = [
    path('', views.TemplateListView.as_view(), name='list'),
    path('category/<slug:slug>/', views.CategoryTemplatesView.as_view(), name='category'),
    path('<slug:slug>/', views.TemplateDetailView.as_view(), name='detail'),
    path('<slug:slug>/demo/', views.GenerateDemoView.as_view(), name='demo'),
    path('<slug:slug>/review/', views.CreateReviewView.as_view(), name='review'),
]