from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from templates.models import Template, Category
from .telegram_service import telegram_bot_service
import logging

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    """
    Home page view with featured templates and statistics
    """
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get featured templates (latest 6 active templates)
        context['featured_templates'] = Template.objects.filter(
            active=True
        ).select_related('category').order_by('-created_at')[:6]
        
        # Get categories
        context['categories'] = Category.objects.all().order_by('name')
        
        # Statistics
        context['stats'] = {
            'total_templates': Template.objects.filter(active=True).count(),
            'categories_count': Category.objects.count(),
            'total_downloads': sum(
                template.download_count for template in Template.objects.all()
            ),
        }
        
        return context


class AboutView(TemplateView):
    """
    About page view
    """
    template_name = 'core/about.html'


class ContactView(TemplateView):
    """
    Contact page view
    """
    template_name = 'core/contact.html'


class DemoBotView(LoginRequiredMixin, View):
    """
    Generate demo bot for template
    """
    
    def post(self, request):
        template_id = request.POST.get('template_id')
        
        if not template_id:
            return JsonResponse({
                'success': False,
                'error': 'Template ID is required'
            })
        
        try:
            template = Template.objects.get(id=template_id, active=True)
        except Template.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Template not found'
            })
        
        # Get user's Telegram username
        user_telegram = getattr(request.user, 'telegram_username', None)
        if not user_telegram:
            user_telegram = f'user_{request.user.id}'
        
        # Create demo bot
        result = telegram_bot_service.create_demo_bot(
            template_id=template.id,
            user_telegram=user_telegram
        )
        
        if result.get('success'):
            logger.info(f'Demo bot created for template {template_id} by user {request.user.id}')
        
        return JsonResponse(result)
