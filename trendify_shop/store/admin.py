from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Product, Order, ShippingOption, UserProfile, ProductVariant, 
    WishList, Cart, CartItem, OrderItem, Payment, Review
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'is_verified_seller', 'seller_rating', 'created_date')
    list_filter = ('role', 'is_verified_seller')
    search_fields = ('user__username', 'store_name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'seller', 'category', 'price', 'status', 'average_rating', 'image_preview')
    list_filter = ('category', 'status', 'created_date')
    search_fields = ('name', 'seller__username')
    readonly_fields = ('image_preview', 'average_rating', 'total_reviews', 'created_date', 'updated_date')

    def image_preview(self, obj):
        if not obj or not obj.image_url:
            return '(no image)'
        return format_html('<img src="{}" style="max-width:120px;max-height:80px;border-radius:8px;"/>', obj.image_url)
    image_preview.short_description = 'Image'


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size', 'color', 'stock', 'sku')
    list_filter = ('product', 'size', 'color')
    search_fields = ('sku', 'product__name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'rating', 'helpful_count', 'created_date')
    list_filter = ('rating', 'created_date')
    search_fields = ('user__username', 'product__name', 'comment')
    readonly_fields = ('created_date', 'updated_date')


@admin.register(ShippingOption)
class ShippingOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'estimated_days', 'carrier')
    search_fields = ('name', 'carrier')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'user', 'status', 'total_cost', 'payment_status', 'ordered_date')
    list_filter = ('status', 'payment_status', 'ordered_date')
    search_fields = ('user__username', 'order_number', 'tracking_number')
    readonly_fields = ('order_number', 'ordered_date', 'updated_date')
    actions = ['mark_processing', 'mark_shipped', 'mark_delivered', 'cancel_order']

    def mark_processing(self, request, queryset):
        updated = queryset.update(status='PROCESSING')
        self.message_user(request, f"{updated} order(s) marked as Processing.")
    mark_processing.short_description = 'Mark selected orders as Processing'

    def mark_shipped(self, request, queryset):
        from django.utils import timezone
        from django.utils.crypto import get_random_string
        count = 0
        for order in queryset:
            if order.status != 'CANCELLED':
                order.status = 'SHIPPED'
                order.shipped_date = timezone.now()
                if not order.tracking_number:
                    order.tracking_number = 'TRK' + get_random_string(12).upper()
                order.save()
                count += 1
        self.message_user(request, f"{count} order(s) marked as Shipped.")
    mark_shipped.short_description = 'Mark selected orders as Shipped'

    def mark_delivered(self, request, queryset):
        updated = queryset.update(status='DELIVERED')
        self.message_user(request, f"{updated} order(s) marked as Delivered.")
    mark_delivered.short_description = 'Mark selected orders as Delivered'

    def cancel_order(self, request, queryset):
        updated = queryset.update(status='CANCELLED')
        self.message_user(request, f"{updated} order(s) marked as Cancelled.")
    cancel_order.short_description = 'Cancel selected orders'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price', 'item_total')
    list_filter = ('order', 'product')
    search_fields = ('order__order_number', 'product__name')
    readonly_fields = ('item_total',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_items', 'total_price', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('user__username',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'total_price')
    list_filter = ('product',)
    search_fields = ('cart__user__username', 'product__name')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'payment_method', 'status', 'timestamp')
    list_filter = ('status', 'payment_method', 'timestamp')
    search_fields = ('order__order_number', 'transaction_id')
    readonly_fields = ('timestamp',)


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product_count', 'created_date')
    search_fields = ('user__username',)
    readonly_fields = ('created_date', 'updated_date')

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'
