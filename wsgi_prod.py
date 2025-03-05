import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# Load production environment variables
load_dotenv('.env.production')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
application = get_wsgi_application() 