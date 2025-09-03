from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Payment
from .serializers import PaymentSerializer, CreatePaymentSerializer, PaymentStatusSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing payments
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreatePaymentSerializer
        elif self.action == 'update_status':
            return PaymentStatusSerializer
        return PaymentSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new payment
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        
        # Return payment data
        response_serializer = PaymentSerializer(payment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        Update payment status (for webhook use)
        """
        payment = self.get_object()
        serializer = PaymentStatusSerializer(payment, data=request.data, partial=True)
        
        if serializer.is_valid():
            # If marking as completed, update processed_at
            if serializer.validated_data.get('status') == 'completed':
                serializer.validated_data['processed_at'] = timezone.now()
                
                # Update order status
                order = payment.order
                order.status = 'completed'
                order.completed_at = timezone.now()
                order.save()
            
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def my_payments(self, request):
        """
        Get current user's payments
        """
        payments = self.get_queryset()
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)