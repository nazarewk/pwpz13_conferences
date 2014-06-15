"""
WSGI config for conferences project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conferences_site.settings")

SITE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(SITE_DIR)

sys.path.insert(0, BASE_DIR)

application = get_wsgi_application()
