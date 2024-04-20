"""
Django command to create a SuperUser and dummy data
"""

import os
from functools import wraps

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


def disable_signals_for_loaddata(signal_handler):
    """
    Decorator that turns off signal handlers when loading fixture data.
    """

    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs.get("raw"):
            return
        signal_handler(*args, **kwargs)

    return wrapper


class Command(BaseCommand):
    """Django command to load fixtures and create superuser if not exists"""

    help = "Load data from fixtures"

    def create_superuser(self):
        self.stdout.write("Creating superuser")
        os.system(
            f"python manage.py loaddata users/fixtures/superuser/001-superuser.json"
        )
        for superuser in User.objects.filter(is_superuser=True):
            superuser.set_password(superuser.password)
            superuser.save()

    @staticmethod
    def get_last_user_id():
        latest_user = User.objects.all().order_by("-id").first()
        return latest_user.id if latest_user else None

    @staticmethod
    def set_new_users_password(latest_old_id):
        new_users = User.objects.all()
        if latest_old_id:
            new_users = new_users.filter(id__gt=latest_old_id)
        for user in new_users:
            user.set_password(user.password)
            user.save()

    @disable_signals_for_loaddata
    def handle(self, *args, **kwargs):
        """Entrypoint for command."""
        self.stdout.write("Loading ")
        if not User.objects.filter(is_superuser=True):
            self.create_superuser()
        else:
            self.stdout.write(self.style.SUCCESS("Superuser exists"))

        latest_old_id = self.get_last_user_id()
        self.stdout.write("Importing data from fixtures")
        apps = ["users", "friends"]
        fixture_full_paths = [f"{app}/fixtures/*.json" for app in apps]
        os.system(f"python manage.py loaddata {' '.join(fixture_full_paths)}")

        self.set_new_users_password(latest_old_id=latest_old_id)
