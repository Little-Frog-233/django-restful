"""
WSGI config for myDjangoRestful project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/

run:
gunicorn --env DJANGO_SETTINGS_MODULE=myDjangoRestful.settings myDjangoRestful.wsgi:application -w 4 -b 0.0.0.0:8000 -k gthread --threads 40 --max-requests 4096 --max-requests-jitter 512
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myDjangoRestful.settings')

application = get_wsgi_application()
