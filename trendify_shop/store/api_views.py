from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg
from datetime import datetime
import uuid

from .models import (
    Product, Order, ShippingOption, UserProfile, ProductVariant,
    WishList, Cart, CartItem, OrderItem, Payment, Review
)
from .serializers import (
    ProductSerializer, ProductDetailSerializer, OrderSerializer, ShippingOptionSerializer,
    UserProfileSerializer, ProductVariantSerializer, WishListSerializer, CartSerializer,
    CartItemSerializer, PaymentSerializer, ReviewSerializer
)

class StandardPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

# User Profile ViewSet
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'

    def get_queryset(self):
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def update_me(self, request):
        """Update current user's profile"""
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Product ViewSet with full CRUD
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(status='ACTIVE').order_by('-created_date')
    pagination_class = StandardPagination
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['created_date', 'price', 'average_rating']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_products(self, request):
        """Get current seller's products"""
        products = Product.objects.filter(seller=request.user)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_variant(self, request, pk=None):
        """Add a variant to product"""
        product = self.get_object()
        if product.seller != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProductVariantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        """Add review to product"""
        product = self.get_object()
        review_data = request.data.copy()
        review_data['user'] = request.user.id
        review_data['product'] = product.id
        
        serializer = ReviewSerializer(data=review_data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            # Update product rating
            avg_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
            product.average_rating = avg_rating or 0
            product.total_reviews = Review.objects.filter(product=product).count()
            product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Product Variant ViewSet
class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.request.data.get('product'))
        if product.seller != self.request.user:
            raise PermissionError('Not authorized')
        serializer.save()

# Review ViewSet
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'user']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# WishList ViewSet
class WishListViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_wishlist(self, request):
        """Get user's wishlist"""
        wishlist, _ = WishList.objects.get_or_create(user=request.user)
        serializer = WishListSerializer(wishlist)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_product(self, request):
        """Add product to wishlist"""
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        wishlist, _ = WishList.objects.get_or_create(user=request.user)
        wishlist.products.add(product)
        serializer = WishListSerializer(wishlist)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def remove_product(self, request):
        """Remove product from wishlist"""
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        wishlist = get_object_or_404(WishList, user=request.user)
        wishlist.products.remove(product)
        serializer = WishListSerializer(wishlist)
        return Response(serializer.data)

# Cart ViewSet
class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_cart(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        """Get user's cart"""
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Add item to cart"""
        cart = self.get_cart(request)
        product_id = request.data.get('product_id')
        variant_id = request.data.get('variant_id')
        quantity = request.data.get('quantity', 1)

        product = get_object_or_404(Product, pk=product_id)
        variant = None
        if variant_id:
            variant = get_object_or_404(ProductVariant, pk=variant_id)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, variant=variant,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def update_item(self, request):
        """Update cart item quantity"""
        cart = self.get_cart(request)
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')

        cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        cart_item.quantity = max(1, int(quantity))
        cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Remove item from cart"""
        cart = self.get_cart(request)
        item_id = request.data.get('item_id')

        cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        cart_item.delete()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def clear_cart(self, request):
        """Clear entire cart"""
        cart = self.get_cart(request)
        cart.items.all().delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().order_by('-ordered_date')
        return Order.objects.filter(user=self.request.user).order_by('-ordered_date')

    def create(self, request, *args, **kwargs):
        """Create order from cart"""
        cart = get_object_or_404(Cart, user=request.user)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        order_data = request.data.copy()
        order_data['user'] = request.user.id
        order_data['order_number'] = str(uuid.uuid4())[:12]

        # Calculate totals
        subtotal = cart.total_price
        tax = subtotal * 0.10  # 10% tax
        shipping_cost = 0
        if 'shipping_option' in order_data:
            shipping = get_object_or_404(ShippingOption, pk=order_data['shipping_option'])
            shipping_cost = shipping.price

        order_data['subtotal'] = subtotal
        order_data['tax'] = tax
        order_data['total_cost'] = subtotal + tax + shipping_cost

        serializer = self.get_serializer(data=order_data)
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            
            # Create order items from cart
            for cart_item in cart.items.all():
                price = cart_item.product.price
                if cart_item.variant and cart_item.variant.price_override:
                    price = cart_item.variant.price_override
                
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    variant=cart_item.variant,
                    quantity=cart_item.quantity,
                    price=price
                )

            # Clear cart
            cart.items.all().delete()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        """Cancel an order"""
        order = self.get_object()
        if order.user != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        if order.status not in ['PENDING', 'PROCESSING']:
            return Response({'error': 'Cannot cancel order'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'CANCELLED'
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

# Shipping Option ViewSet
class ShippingOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ShippingOption.objects.all()
    serializer_class = ShippingOptionSerializer
    permission_classes = [AllowAny]

# Payment ViewSet
class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def process_payment(self, request):
        """Process payment for order"""
        order_id = request.data.get('order_id')
        payment_method = request.data.get('payment_method')
        
        order = get_object_or_404(Order, pk=order_id, user=request.user)
        if order.status != 'PENDING':
            return Response({'error': 'Invalid order status'}, status=status.HTTP_400_BAD_REQUEST)

        # Create payment record
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                'amount': order.total_cost,
                'payment_method': payment_method,
                'status': 'COMPLETED',
                'transaction_id': str(uuid.uuid4())
            }
        )

        if payment.status == 'COMPLETED':
            order.status = 'PROCESSING'
            order.payment_status = 'COMPLETED'
            order.payment_method = payment_method
            order.transaction_id = payment.transaction_id
            order.save()

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
