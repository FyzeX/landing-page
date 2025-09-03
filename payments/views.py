from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse
from .models import Payment
from orders.models import Order
import json
from datetime import datetime


class ProcessPaymentView(LoginRequiredMixin, TemplateView):
    """
    Payment processing page
    """
    template_name = 'payments/process.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.GET.get('order_id')
        
        if order_id:
            try:
                context['order'] = Order.objects.get(
                    id=order_id, 
                    user=self.request.user, 
                    status='created'
                )
            except Order.DoesNotExist:
                pass
        
        return context
    
    def post(self, request):
        order_id = request.POST.get('order_id')
        payment_method = request.POST.get('payment_method')
        
        if not order_id or not payment_method:
            messages.error(request, 'Invalid payment data')
            return redirect('templates:list')
        
        order = get_object_or_404(
            Order, 
            id=order_id, 
            user=request.user, 
            status='created'
        )
        
        # Create payment record
        payment = Payment.objects.create(
            order=order,
            payment_method=payment_method,
            amount=order.amount,
            currency=order.currency,
            status='pending'
        )
        
        # Update order status
        order.status = 'pending'
        order.save()
        
        # TODO: Integrate with actual payment gateways
        # For demo purposes, simulate successful payment
        if payment_method == 'telegram':
            return self._simulate_telegram_payment(payment)
        else:
            return self._simulate_crypto_payment(payment)
    
    def _simulate_telegram_payment(self, payment):
        """
        Simulate Telegram payment (for demo)
        """
        # In real implementation, redirect to Telegram payment
        payment.status = 'completed'
        payment.transaction_id = f'tg_{payment.id}'
        payment.processed_at = datetime.now()
        payment.save()
        
        # Complete order
        order = payment.order
        order.status = 'completed'
        order.completed_at = datetime.now()
        order.save()
        
        messages.success(self.request, 'Payment completed successfully!')
        return redirect('payments:success', order_id=order.id)
    
    def _simulate_crypto_payment(self, payment):
        """
        Simulate crypto payment (for demo)
        """
        # In real implementation, generate crypto address and wait for payment
        payment.status = 'completed'
        payment.transaction_id = f'crypto_{payment.id}'
        payment.processed_at = datetime.now()
        payment.save()
        
        # Complete order
        order = payment.order
        order.status = 'completed'
        order.completed_at = datetime.now()
        order.save()
        
        messages.success(self.request, 'Payment completed successfully!')
        return redirect('payments:success', order_id=order.id)


class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    """
    Payment success page
    """
    template_name = 'payments/success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['order_id']
        
        context['order'] = get_object_or_404(
            Order, 
            id=order_id, 
            user=self.request.user, 
            status='completed'
        )
        
        return context


class PaymentCancelView(LoginRequiredMixin, TemplateView):
    """
    Payment cancellation page
    """
    template_name = 'payments/cancel.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['order_id']
        
        try:
            order = Order.objects.get(id=order_id, user=self.request.user)
            context['order'] = order
            
            # Update order status if it was pending
            if order.status == 'pending':
                order.status = 'failed'
                order.save()
                
                # Update payment status
                try:
                    payment = order.payment
                    payment.status = 'cancelled'
                    payment.save()
                except Payment.DoesNotExist:
                    pass
        except Order.DoesNotExist:
            pass
        
        return context


@method_decorator(csrf_exempt, name='dispatch')
class TelegramWebhookView(View):
    """
    Webhook for Telegram payment notifications
    """
    def post(self, request):
        try:
            data = json.loads(request.body)
            # TODO: Process Telegram webhook data
            # Verify signature, update payment status, etc.
            
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
