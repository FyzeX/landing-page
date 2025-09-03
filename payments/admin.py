from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'order_link', 'payment_method', 'amount', 
        'status', 'transaction_id', 'created_at'
    ]
    list_filter = ['payment_method', 'status', 'currency', 'created_at']
    search_fields = [
        'id', 'transaction_id', 'order__user__username', 
        'order__template__title'
    ]
    readonly_fields = [
        'id', 'created_at', 'processed_at', 
        'gateway_response_formatted'
    ]
    
    fieldsets = (
        ('Payment Information', {
            'fields': (
                'id', 'order', 'payment_method', 
                'transaction_id', 'amount', 'currency'
            )
        }),
        ('Status & Timestamps', {
            'fields': ('status', 'created_at', 'processed_at')
        }),
        ('Gateway Response', {
            'fields': ('gateway_response_formatted',),
            'classes': ('collapse',)
        })
    )
    
    def order_link(self, obj):
        url = reverse('admin:orders_order_change', args=[obj.order.pk])
        return format_html(
            '<a href="{}">{}</a>', 
            url, str(obj.order.id)[:8] + '...'
        )
    order_link.short_description = 'Order'
    
    def gateway_response_formatted(self, obj):
        if obj.gateway_response:
            import json
            return format_html(
                '<pre>{}</pre>', 
                json.dumps(obj.gateway_response, indent=2)
            )
        return "No response data"
    gateway_response_formatted.short_description = 'Gateway Response'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order')
