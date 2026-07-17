from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('men/', views.men_view, name='men'),
    path('women/', views.women_view, name='women'),
    path('kids/', views.kids_view, name='kids'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('contact/', views.contact_view, name='contact'),
    path('orders/', views.orders_view, name='orders'),
    path('place-order/', views.place_order, name='place_order'),
    path('receipt/<int:order_id>/', views.receipt_view, name='receipt'),
]