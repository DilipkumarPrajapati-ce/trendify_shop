from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Order, ShippingOption
from .serializers import ProductSerializer, OrderSerializer, ShippingOptionSerializer
from rest_framework.permissions import IsAuthenticated

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class ShippingOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ShippingOption.objects.all()
    serializer_class = ShippingOptionSerializer
    permission_classes = [permissions.AllowAny]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-ordered_date')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # set user and compute shipping cost if shipping option provided
        shipping_option = serializer.validated_data.get('shipping_option', None)
        shipping_cost = 0
        if shipping_option:
            shipping_cost = shipping_option.price
        serializer.save(user=self.request.user, shipping_cost=shipping_cost)

    def get_queryset(self):
        # restrict orders to user
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().order_by('-ordered_date')
        return Order.objects.filter(user=user).order_by('-ordered_date')

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_shipped(self, request, pk=None):
        order = self.get_object()
        order.status = 'Shipped'
        order.save()
        return Response({'status': 'shipped'})
