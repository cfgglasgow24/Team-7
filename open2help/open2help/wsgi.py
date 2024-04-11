"""
WSGI config for open2help project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# defaulting to open2help settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'open2help.settings')

# WSGI module-level variable
application = get_wsgi_application()
