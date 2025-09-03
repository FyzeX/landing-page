from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user_link', 'template_link', 'amount', 
        'status', 'download_count', 'created_at'
    ]
    list_filter = ['status', 'created_at', 'completed_at']
    search_fields = [
        'id', 'user__username', 'user__email', 
        'template__title'
    ]
    readonly_fields = [
        'id', 'download_token', 'created_at', 
        'completed_at', 'payment_link'
    ]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'user', 'template', 'amount', 'currency')
        }),
        ('Status & Downloads', {
            'fields': ('status', 'download_count', 'max_downloads', 'download_token')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at')
        }),
        ('Payment', {
            'fields': ('payment_link',)
        })
    )
    
    def user_link(self, obj):
        url = reverse('admin:users_user_change', args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    def template_link(self, obj):
        url = reverse('admin:templates_template_change', args=[obj.template.pk])
        return format_html('<a href="{}">{}</a>', url, obj.template.title)
    template_link.short_description = 'Template'
    
    def payment_link(self, obj):
        try:
            payment = obj.payment
            url = reverse('admin:payments_payment_change', args=[payment.pk])
            return format_html(
                '<a href="{}">{} - {}</a>', 
                url, payment.payment_method, payment.status
            )
        except:
            return "No payment"
    payment_link.short_description = 'Payment'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'template'
        )
