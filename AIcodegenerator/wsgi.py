"""
WSGI config for AIcodegenerator project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

# -------- Addition for environment variables
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
# -------------------------------------------

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AIcodegenerator.settings")

application = get_wsgi_application()
