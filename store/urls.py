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
    path('receipt/<int:order_id>/', views.receipt_view, name='receipt'),
]