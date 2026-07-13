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