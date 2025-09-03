from rest_framework import serializers
from .models import Order
from templates.serializers import TemplateListSerializer


class OrderSerializer(serializers.ModelSerializer):
    template = TemplateListSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    can_download = serializers.ReadOnlyField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'template', 'amount', 'currency', 'status',
            'download_count', 'max_downloads', 'created_at', 'completed_at',
            'can_download'
        ]


class CreateOrderSerializer(serializers.ModelSerializer):
    template_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Order
        fields = ['template_id']
        
    def create(self, validated_data):
        from templates.models import Template
        
        template_id = validated_data.pop('template_id')
        template = Template.objects.get(id=template_id, active=True)
        
        order = Order.objects.create(
            user=self.context['request'].user,
            template=template,
            amount=template.price,
            status='created'
        )
        return order