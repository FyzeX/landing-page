from rest_framework import serializers
from .models import Template, Category, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon']


class TemplateSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    average_rating = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Template
        fields = [
            'id', 'title', 'slug', 'description', 'short_description', 
            'price', 'category', 'thumbnail', 'features', 'demo_available',
            'active', 'created_at', 'updated_at', 'download_count',
            'average_rating', 'review_count'
        ]


class TemplateListSerializer(serializers.ModelSerializer):
    """Simplified serializer for template lists"""
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Template
        fields = [
            'id', 'title', 'slug', 'short_description', 'price', 
            'category', 'thumbnail', 'demo_available', 'download_count'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    template = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'template', 'rating', 'comment', 'created_at']


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['template'] = self.context['template']
        return super().create(validated_data)