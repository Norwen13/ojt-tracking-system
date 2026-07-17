from django.core.management.base import BaseCommand
from placement.models import SchoolAdmin


class Command(BaseCommand):
    help = "Creates (or resets) a School Admin account so you can log in for the first time."

    def add_arguments(self, parser):
        parser.add_argument("--password", default="admin123", help="Password for the admin account.")

    def handle(self, *args, **options):
        password = options["password"]
        admin, created = SchoolAdmin.objects.get_or_create(pk=1)
        admin.set_password(password)
        admin.save()
        action = "Created" if created else "Reset"
        self.stdout.write(self.style.SUCCESS(
            f"{action} School Admin account -> admin_id: {admin.admin_id}, password: {password}"
        ))


import os
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not all([username, email, password]):
            self.stdout.write("Superuser env vars incomplete; skipped.")
            return
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write("Superuser created successfully.")
        else:
            self.stdout.write("Superuser already exists.")