from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


def create(fields):
    with transaction.atomic():
        user = User.objects.create_user(**fields)
        if settings.SEND_ACTIVATION_EMAIL:
            user.is_active = False
            user.save(update_fields=["is_active"])
    return user


def get(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def exist(email):
    return User.objects.filter(email=email).exists()


def is_active(email):
    user = get(email)
    if not user:
        return False
    return user.is_active
