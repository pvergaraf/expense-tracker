"""
WSGI config for chiwismo project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# Load production environment variables
load_dotenv('.env.production')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chiwismo_config.settings')
application = get_wsgi_application() 