from django.db.models.signals import post_migrate
from django.apps import apps
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_shipping_options(sender, **kwargs):
    # Only run for the 'store' app
    try:
        label = sender.label
    except Exception:
        return
    if label != 'store':
        return

    ShippingOption = apps.get_model('store', 'ShippingOption')
    if not ShippingOption:
        return

    if ShippingOption.objects.exists():
        return

    defaults = [
        {'name': 'Standard', 'price': '49.00', 'estimated_days': 5, 'carrier': 'Local Post'},
        {'name': 'Express', 'price': '149.00', 'estimated_days': 2, 'carrier': 'FastShip'},
        {'name': 'Overnight', 'price': '299.00', 'estimated_days': 1, 'carrier': 'QuickOvernight'},
    ]
    for opt in defaults:
        try:
            ShippingOption.objects.create(**opt)
        except Exception:
            continue

    Product = apps.get_model('store', 'Product')
    if Product and not Product.objects.exists():
        demo_products = [
            {'name': 'Aurora Silk Shirt', 'price': '899.00', 'category': 'MEN', 'image_url': 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Nova Trim Blouse', 'price': '749.00', 'category': 'WOMEN', 'image_url': 'https://images.unsplash.com/photo-1520975911700-0e7a0d383cad?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Mini Groove Hoodie', 'price': '499.00', 'category': 'KIDS', 'image_url': 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Midtown Denim Jacket', 'price': '1299.00', 'category': 'MEN', 'image_url': 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Luna Lounge Set', 'price': '1099.00', 'category': 'WOMEN', 'image_url': 'https://images.unsplash.com/photo-1520975911700-0e7a0d383cad?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Playtime Polo', 'price': '349.00', 'category': 'KIDS', 'image_url': 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=800&q=80'},
        ]
        for item in demo_products:
            try:
                Product.objects.create(**item)
            except Exception:
                continue