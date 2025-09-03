from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Template, Category, Review
from .serializers import TemplateSerializer, CategorySerializer, ReviewSerializer


class TemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for templates (read-only)
    """
    queryset = Template.objects.filter(active=True)
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at', 'download_count']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Get featured templates
        """
        featured_templates = self.get_queryset().filter(featured=True)[:6]
        serializer = self.get_serializer(featured_templates, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """
        Get popular templates by download count
        """
        popular_templates = self.get_queryset().order_by('-download_count')[:10]
        serializer = self.get_serializer(popular_templates, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for categories (read-only)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for reviews
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        template_id = self.request.query_params.get('template_id')
        if template_id:
            return Review.objects.filter(template_id=template_id, approved=True)
        return Review.objects.filter(approved=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)