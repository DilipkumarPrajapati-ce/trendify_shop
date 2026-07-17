from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = 'Seed demo products for Trendify'

    def handle(self, *args, **options):
        demo = [
            {'name': 'Aurora Silk Shirt', 'price': '899.00', 'category': 'MEN', 'image_url': 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=1200&q=80'},
            {'name': 'Luna Lounge Set', 'price': '1099.00', 'category': 'WOMEN', 'image_url': 'https://images.unsplash.com/photo-1520975911700-0e7a0d383cad?auto=format&fit=crop&w=1200&q=80'},
        ]
        for item in demo:
            obj, created = Product.objects.get_or_create(name=item['name'], defaults={'price':item['price'], 'category':item['category'], 'image_url':item['image_url']})
            if not created:
                obj.image_url = item['image_url']
                obj.price = item['price']
                obj.category = item['category']
                obj.save()
            self.stdout.write(self.style.SUCCESS(f'Product ensured: {obj.name} (id={obj.id})'))
