import pytest
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
from django.urls import reverse

from .factories import UserFactory

User = get_user_model()


@pytest.mark.django_db
def test_register(client):
    email = "test@test.com"
    data = {"email": email, "password": "pass1234word", "timezone": "America/New_York"}

    url = reverse("users:register")
    response = client.post(url, data=data, content_type="application/json")

    assert response.status_code == 201

    user = User.objects.get(email=email)
    assert user.is_active
    assert str(user.timezone) == "America/New_York"


@override_settings(SEND_ACTIVATION_EMAIL=True)
@pytest.mark.django_db
def test_register_in_not_active(client):
    email = "test@test.com"
    data = {"email": email, "password": "pass1234word"}

    url = reverse("users:register")
    response = client.post(url, data=data, content_type="application/json")

    assert response.status_code == 201

    user = User.objects.get(email=email)
    assert not user.is_active
    assert str(user.timezone) == "UTC"


@pytest.mark.django_db
def test_register_invalid_password(client):

    data = {"email": "test@test.com", "password": "password"}

    url = reverse("users:register")
    response = client.post(url, data=data, content_type="application/json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_register_invalid_timezone(client):

    data = {"email": "test@test.com", "password": "pass1234word", "timezone": "Wrong"}

    url = reverse("users:register")
    response = client.post(url, data=data, content_type="application/json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_login(client):
    user = UserFactory(password="testing")

    data = {"email": user.email, "password": "testing"}

    url = reverse("users:login")
    response = client.post(url, data=data, content_type="application/json")

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_wrong_email(client):
    data = {"email": "wrong@email.com", "password": "testing"}

    url = reverse("users:login")
    response = client.post(url, data=data, content_type="application/json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_wrong_password(client):
    user = UserFactory(password="testing")

    data = {"email": user.email, "password": "wrong"}

    url = reverse("users:login")
    response = client.post(url, data=data, content_type="application/json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_not_active(client):
    user = UserFactory(password="testing", is_active=False)

    data = {"email": user.email, "password": "testing"}

    url = reverse("users:login")
    response = client.post(url, data=data, content_type="application/json")

    assert response.status_code == 400
