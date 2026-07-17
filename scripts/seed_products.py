from store.models import Product

name='Hoodie Mockup'
img='https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=800&q=80'
product, created = Product.objects.get_or_create(name=name, defaults={'price':'799.00','category':'MEN','image_url':img})
if not created:
    product.image_url = img
    product.price = '799.00'
    product.category = 'MEN'
    product.save()
print('product:', product.id, product.name)
