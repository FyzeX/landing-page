from rest_framework import serializers
from .models import Payment
from orders.serializers import OrderSerializer


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment model
    """
    order = OrderSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'payment_method', 'amount', 'currency',
            'status', 'transaction_id', 'gateway_response',
            'created_at', 'processed_at'
        ]
        read_only_fields = ['id', 'created_at', 'processed_at']


class CreatePaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for creating payments
    """
    order_id = serializers.UUIDField()
    
    class Meta:
        model = Payment
        fields = ['order_id', 'payment_method']
    
    def validate_order_id(self, value):
        from orders.models import Order
        try:
            order = Order.objects.get(id=value, status='created')
            return value
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found or already processed")
    
    def create(self, validated_data):
        from orders.models import Order
        order_id = validated_data.pop('order_id')
        order = Order.objects.get(id=order_id)
        
        payment = Payment.objects.create(
            order=order,
            amount=order.amount,
            currency=order.currency,
            **validated_data
        )
        
        # Update order status
        order.status = 'pending'
        order.save()
        
        return payment


class PaymentStatusSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for payment status updates
    """
    class Meta:
        model = Payment
        fields = ['id', 'status', 'transaction_id', 'processed_at']
        read_only_fields = ['id']