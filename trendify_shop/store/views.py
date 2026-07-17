from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Order, ShippingOption, Review, ContactMessage
from .forms import ReviewForm, ContactMessageForm

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
    # show a primary featured product on the home page
    featured_products = list(Product.objects.order_by('id')[:2])
    primary_featured = featured_products[0] if featured_products else None
    return render(request, 'home.html', {
        'featured_products': featured_products,
        'primary_featured': primary_featured,
    })

# Men's Clothing Page
@login_required(login_url='login')
def men_view(request):
    products = Product.objects.filter(category='MEN')
    shipping_options = ShippingOption.objects.all()
    return render(request, 'men.html', {
        'products': products,
        'shipping_options': shipping_options,
    })

# Women's Clothing Page
@login_required(login_url='login')
def women_view(request):
    products = Product.objects.filter(category='WOMEN')
    shipping_options = ShippingOption.objects.all()
    return render(request, 'women.html', {
        'products': products,
        'shipping_options': shipping_options,
    })

# Kids' Clothing Page
@login_required(login_url='login')
def kids_view(request):
    products = Product.objects.filter(category='KIDS')
    shipping_options = ShippingOption.objects.all()
    return render(request, 'kids.html', {
        'products': products,
        'shipping_options': shipping_options,
    })

# Interactive Digital Receipt Generator
@login_required(login_url='login')
def receipt_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'receipt.html', {'order': order})

# Create a new order and redirect to receipt
@login_required(login_url='login')
def place_order(request):
    if request.method != 'POST':
        return redirect('home')

    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity') or 1)
    shipping_id = request.POST.get('shipping_option')
    shipping_option = ShippingOption.objects.filter(id=shipping_id).first()
    product = get_object_or_404(Product, id=product_id)

    if not shipping_option:
        shipping_option = ShippingOption.objects.filter(name='Standard').first()

    shipping_cost = shipping_option.price if shipping_option else 0
    order = Order.objects.create(
        user=request.user,
        product=product,
        quantity=quantity,
        shipping_option=shipping_option,
        shipping_address=request.POST.get('shipping_address', '').strip(),
        shipping_cost=shipping_cost,
        status='Processing'
    )
    return redirect('receipt', order_id=order.id)

# Order history list for logged-in users
@login_required(login_url='login')
def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'orders.html', {'orders': orders})

# Dashboard page for user overview
@login_required(login_url='login')
def dashboard_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_date')[:4]
    order_count = Order.objects.filter(user=request.user).count()
    total_spent = sum(order.total_cost for order in Order.objects.filter(user=request.user))
    return render(request, 'dashboard.html', {
        'orders': orders,
        'order_count': order_count,
        'total_spent': total_spent,
    })

# Profile dashboard with account summary
@login_required(login_url='login')
def profile_view(request):
    order_count = Order.objects.filter(user=request.user).count()
    latest_order = Order.objects.filter(user=request.user).order_by('-ordered_date').first()
    return render(request, 'profile.html', {
        'order_count': order_count,
        'latest_order': latest_order,
    })

# Contact page with support details
@login_required(login_url='login')
def contact_view(request):
    contact_form = ContactMessageForm(request.POST or None)
    review_form = ReviewForm(request.POST or None)
    if request.method == 'POST':
        if 'contact_submit' in request.POST and contact_form.is_valid():
            contact_message = contact_form.save(commit=False)
            contact_message.user = request.user
            contact_message.save()
            return redirect('contact')
        if 'review_submit' in request.POST and review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('contact')

    recent_reviews = Review.objects.order_by('-created_date')[:5]
    return render(request, 'contact.html', {
        'contact_form': contact_form,
        'review_form': review_form,
        'recent_reviews': recent_reviews,
    })