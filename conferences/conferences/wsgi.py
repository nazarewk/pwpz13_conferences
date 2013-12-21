"""
WSGI config for conferences project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conferences.settings")

SITE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJ_DIR = os.path.dirname(SITE_DIR)

sys.path.insert(0, PROJ_DIR)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
