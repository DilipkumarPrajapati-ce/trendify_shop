from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import api_views

router = DefaultRouter()
router.register(r'products', api_views.ProductViewSet, basename='product')
router.register(r'variants', api_views.ProductVariantViewSet, basename='variant')
router.register(r'reviews', api_views.ReviewViewSet, basename='review')
router.register(r'shipping', api_views.ShippingOptionViewSet, basename='shipping')
router.register(r'orders', api_views.OrderViewSet, basename='order')
router.register(r'profiles', api_views.UserProfileViewSet, basename='profile')
router.register(r'wishlist', api_views.WishListViewSet, basename='wishlist')
router.register(r'cart', api_views.CartViewSet, basename='cart')
router.register(r'payments', api_views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]
