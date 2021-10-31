"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from pictionary_db.models import Category, TempCategory

# startup code
while len(TempCategory.objects.all()) < 5:
    s = Category.objects.random()
    if not TempCategory.objects.filter(name=s).exists():
        TempCategory.objects.create(name=s)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
