import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','jobhunting.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    u = User.objects.get(username='admin')
    u.set_password('admin')
    u.save()
    print('password set')
except Exception as e:
    print('error:', e)
