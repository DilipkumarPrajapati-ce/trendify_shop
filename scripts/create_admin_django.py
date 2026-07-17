from django.contrib.auth import get_user_model
User = get_user_model()
username='admin'
email='admin@example.com'
password='Trendify123!'
user, created = User.objects.get_or_create(username=username, defaults={'email':email,'is_staff':True,'is_superuser':True})
if not created:
    user.email=email
    user.is_staff=True
    user.is_superuser=True
user.set_password(password)
user.save()
print('superuser created/updated:', user.username)
