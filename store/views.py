from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Order

# Signup/Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Automatically logs user in upon registration
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Secure Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout Action
def logout_view(request):
    logout(request)
    return redirect('login')

# Main landing dashboard dashboard 
@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

# Men's Clothing Page
@login_required(login_url='login')
def men_view(request):
    products = Product.objects.filter(category='MEN')
    return render(request, 'men.html', {'products': products})

# Women's Clothing Page
@login_required(login_url='login')
def women_view(request):
    products = Product.objects.filter(category='WOMEN')
    return render(request, 'women.html', {'products': products})

# Kids' Clothing Page
@login_required(login_url='login')
def kids_view(request):
    products = Product.objects.filter(category='KIDS')
    return render(request, 'kids.html', {'products': products})

# Interactive Digital Receipt Generator
@login_required(login_url='login')
def receipt_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        return render(request, 'receipt.html', {'order': order})
    except Order.DoesNotExist:
        return redirect('home')