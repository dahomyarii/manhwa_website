import os
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manhwa_website.settings")
django.setup()

call_command("createsuperuser", interactive=False, username="dahomyarii-admin", email="dahomyarii@hotmail.com", password="Forever12@")
