from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Order, ShippingOption

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','price','category','image_url']

class ShippingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingOption
        fields = ['id','name','price','estimated_days','carrier']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = Order
        fields = ['id','user','product','product_id','quantity','ordered_date','status','shipping_option','shipping_address','shipping_cost','shipped_date','tracking_number']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']
