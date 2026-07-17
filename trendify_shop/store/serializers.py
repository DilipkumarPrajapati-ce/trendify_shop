from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Product, Order, ShippingOption, UserProfile, ProductVariant, 
    WishList, Cart, CartItem, OrderItem, Payment, Review
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role', 'bio', 'profile_picture', 'phone', 'address', 
                  'city', 'state', 'postal_code', 'country', 'store_name', 
                  'store_description', 'is_verified_seller', 'seller_rating', 'created_date']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'size', 'color', 'stock', 'sku', 'price_override', 'created_date']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'title', 'comment', 'helpful_count', 'created_date']

class ProductSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'seller', 'name', 'description', 'price', 'category', 'image_url', 
                  'status', 'average_rating', 'total_reviews', 'variants', 'reviews', 'created_date']

class ProductDetailSerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'

class ShippingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingOption
        fields = ['id', 'name', 'price', 'estimated_days', 'carrier']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    variant = ProductVariantSerializer(read_only=True)
    variant_id = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all(), source='variant', write_only=True, required=False)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'variant', 'variant_id', 'quantity', 'total_price', 'added_date']
    
    def get_total_price(self, obj):
        return obj.total_price

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'total_items', 'created_date', 'updated_date']
    
    def get_total_price(self, obj):
        return obj.total_price
    
    def get_total_items(self, obj):
        return obj.total_items

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'variant', 'quantity', 'price', 'item_total']

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_option = ShippingOptionSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'order_number', 'status', 'items', 'shipping_option', 
                  'shipping_address', 'shipping_cost', 'subtotal', 'tax', 'discount', 
                  'total_cost', 'payment_method', 'payment_status', 'ordered_date', 'updated_date']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'payment_method', 'status', 'transaction_id', 'timestamp']

class WishListSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='products',
        many=True,
        write_only=True
    )
    
    class Meta:
        model = WishList
        fields = ['id', 'products', 'product_ids', 'created_date', 'updated_date']
