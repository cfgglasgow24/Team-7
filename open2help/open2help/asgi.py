"""
ASGI config for open2help project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# defaulting environment settings to open2help.settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'open2help.settings')

# defining application as callable module-level variable
application = get_asgi_application()
