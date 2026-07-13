from django.contrib import admin
from .models import Product, Order, ShippingOption


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'category', 'price')
	list_filter = ('category',)
	search_fields = ('name',)


@admin.register(ShippingOption)
class ShippingOptionAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'price', 'estimated_days', 'carrier')
	search_fields = ('name', 'carrier')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'product', 'quantity', 'status', 'shipping_option', 'shipping_cost', 'ordered_date')
	list_filter = ('status', 'shipping_option')
	search_fields = ('user__username', 'product__name', 'tracking_number')
	readonly_fields = ('ordered_date',)
	actions = ['approve_order', 'mark_shipped']

	def approve_order(self, request, queryset):
		updated = queryset.update(status='Approved')
		self.message_user(request, f"{updated} order(s) marked as Approved.")
	approve_order.short_description = 'Mark selected orders as Approved'

	def mark_shipped(self, request, queryset):
		from django.utils import timezone
		from django.utils.crypto import get_random_string
		count = 0
		for order in queryset:
			order.status = 'Shipped'
			order.shipped_date = timezone.now()
			if not order.tracking_number:
				order.tracking_number = 'TRK' + get_random_string(12).upper()
			order.save()
			count += 1
		self.message_user(request, f"{count} order(s) marked as Shipped.")
	mark_shipped.short_description = 'Mark selected orders as Shipped (set date & tracking)'
