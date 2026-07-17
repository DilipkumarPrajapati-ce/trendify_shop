from store.models import Product
for p in Product.objects.all():
    print(p.id, p.name, p.image_url)
