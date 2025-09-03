from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.urls import reverse_lazy
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer, CreateOrderSerializer
from templates.models import Template
from payments.models import Payment


class OrderListView(LoginRequiredMixin, ListView):
    """
    User's order history
    """
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).select_related('template', 'template__category').order_by('-created_at')


class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    Order detail view
    """
    model = Order
    template_name = 'orders/detail.html'
    context_object_name = 'order'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related(
            'template', 'template__category'
        )


class CreateOrderView(LoginRequiredMixin, View):
    """
    Create a new order
    """
    def post(self, request):
        template_id = request.POST.get('template_id')
        if not template_id:
            messages.error(request, 'Template not specified')
            return redirect('templates:list')
        
        template = get_object_or_404(Template, id=template_id, active=True)
        
        # Check if user already owns this template
        if Order.objects.filter(
            user=request.user, 
            template=template, 
            status='completed'
        ).exists():
            messages.info(request, 'You already own this template')
            return redirect('templates:detail', slug=template.slug)
        
        # Create new order
        order = Order.objects.create(
            user=request.user,
            template=template,
            amount=template.price,
            status='created'
        )
        
        messages.success(request, 'Order created! Proceed to payment.')
        return redirect('payments:process') + f'?order_id={order.id}'


class DownloadTemplateView(LoginRequiredMixin, View):
    """
    Download purchased template
    """
    def get(self, request, token):
        order = get_object_or_404(
            Order, 
            download_token=token, 
            user=request.user, 
            status='completed'
        )
        
        if not order.can_download:
            messages.error(request, 'Download limit exceeded or order not completed')
            return redirect('orders:detail', pk=order.pk)
        
        # Increment download count
        order.increment_download_count()
        
        # TODO: Implement actual file download
        # For now, return a simple response
        response = HttpResponse(
            f"Download link for {order.template.title}. "
            f"Downloads remaining: {order.max_downloads - order.download_count}",
            content_type="text/plain"
        )
        response['Content-Disposition'] = f'attachment; filename="{order.template.slug}.txt"'
        return response
