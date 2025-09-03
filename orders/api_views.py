from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Order
from .serializers import OrderSerializer, CreateOrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing orders
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new order
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=request.user)
        
        # Return order data
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        """
        Cancel an order
        """
        order = self.get_object()
        
        if order.status != 'created':
            return Response(
                {'error': 'Only pending orders can be cancelled'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'cancelled'
        order.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Generate download link for completed order
        """
        order = self.get_object()
        
        if order.status != 'completed':
            return Response(
                {'error': 'Order must be completed to download'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate download token (would normally be a secure token)
        download_token = order.generate_download_token()
        
        return Response({
            'download_url': f'/orders/{order.id}/download/{download_token}/',
            'expires_at': timezone.now() + timezone.timedelta(hours=24)
        })
    
    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """
        Get current user's orders
        """
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)