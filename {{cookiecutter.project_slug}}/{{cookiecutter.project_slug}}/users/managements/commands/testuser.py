from django.contrib.auth import forms, get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Creates a new superuser"

    def handle(self, **options):

        User.objects.create_superuser("test@test.com", "test")
        self.stderr.write("Successfully created a new user:\n")
        self.stderr.write("    Username: test@test.com\n")
        self.stderr.write("    Password: test\n")
