from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Template, Category, Review
from .forms import ReviewForm
from .serializers import (
    TemplateSerializer, TemplateListSerializer, CategorySerializer, 
    ReviewSerializer, CreateReviewSerializer
)


class TemplateListView(ListView):
    """
    Template catalog with filtering and search
    """
    model = Template
    template_name = 'templates/list.html'
    context_object_name = 'templates'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Template.objects.filter(active=True).select_related('category')
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(short_description__icontains=search)
            )
        
        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Price filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        valid_sorts = ['-created_at', 'created_at', 'price', '-price', 'title', '-title']
        if sort in valid_sorts:
            queryset = queryset.order_by(sort)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        context['current_search'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        return context


class CategoryTemplatesView(TemplateListView):
    """
    Templates filtered by category
    """
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return super().get_queryset().filter(category=self.category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TemplateDetailView(DetailView):
    """
    Template detail page with reviews and purchase option
    """
    model = Template
    template_name = 'templates/detail.html'
    context_object_name = 'template'
    
    def get_queryset(self):
        return Template.objects.filter(active=True).select_related('category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        template = self.object
        
        # Get reviews
        context['reviews'] = template.reviews.select_related('user').order_by('-created_at')
        context['review_form'] = ReviewForm()
        
        # Related templates
        context['related_templates'] = Template.objects.filter(
            category=template.category,
            active=True
        ).exclude(id=template.id)[:3]
        
        return context


class CreateReviewView(LoginRequiredMixin, CreateView):
    """
    Create a review for a template
    """
    model = Review
    form_class = ReviewForm
    
    def form_valid(self, form):
        template = get_object_or_404(Template, slug=self.kwargs['slug'])
        
        # Check if user already reviewed this template
        if Review.objects.filter(user=self.request.user, template=template).exists():
            messages.error(self.request, 'You have already reviewed this template.')
            return redirect('templates:detail', slug=template.slug)
        
        form.instance.user = self.request.user
        form.instance.template = template
        messages.success(self.request, 'Thank you for your review!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.template.get_absolute_url()


class GenerateDemoView(View):
    """
    Generate demo bot for a template
    """
    def post(self, request, slug):
        template = get_object_or_404(Template, slug=slug, active=True)
        
        if not template.demo_available:
            return JsonResponse({
                'success': False,
                'message': 'Demo is not available for this template'
            })
        
        # TODO: Implement actual demo bot generation
        # For now, return a mock response
        import uuid
        from datetime import datetime, timedelta
        
        demo_username = f"demo_{template.slug}_{uuid.uuid4().hex[:8]}"
        expires_at = datetime.now() + timedelta(hours=24)
        
        return JsonResponse({
            'success': True,
            'bot_username': demo_username,
            'expires_at': expires_at.isoformat(),
            'message': 'Demo bot generated successfully'
        })


# REST API ViewSets
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet for categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class TemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet for templates
    """
    queryset = Template.objects.filter(active=True)
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TemplateListSerializer
        return TemplateSerializer
    
    def get_queryset(self):
        queryset = Template.objects.filter(active=True).select_related('category')
        
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(short_description__icontains=search)
            )
        
        # Category filter
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Price filter
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, slug=None):
        """Get reviews for a specific template"""
        template = self.get_object()
        reviews = template.reviews.select_related('user').order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for reviews
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateReviewSerializer
        return ReviewSerializer
    
    def perform_create(self, serializer):
        template_slug = self.request.data.get('template_slug')
        template = get_object_or_404(Template, slug=template_slug)
        serializer.save(user=self.request.user, template=template)


class GenerateDemoAPIView(APIView):
    """
    API endpoint for generating demo bots
    """
    def post(self, request, slug):
        template = get_object_or_404(Template, slug=slug, active=True)
        
        if not template.demo_available:
            return Response({
                'success': False,
                'message': 'Demo is not available for this template'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # TODO: Implement actual demo bot generation
        # For now, return a mock response
        import uuid
        from datetime import datetime, timedelta
        
        demo_username = f"demo_{template.slug}_{uuid.uuid4().hex[:8]}"
        expires_at = datetime.now() + timedelta(hours=24)
        
        return Response({
            'success': True,
            'bot_username': demo_username,
            'expires_at': expires_at.isoformat(),
            'message': 'Demo bot generated successfully'
        })
