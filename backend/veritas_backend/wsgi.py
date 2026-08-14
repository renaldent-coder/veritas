"""
WSGI config for veritas_backend project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os
import sys  # 👈 ADD THIS
from django.core.wsgi import get_wsgi_application

# 👇 ADD THIS LINE — tells Python where to find the 'apps' folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veritas_backend.settings')

application = get_wsgi_application()