from django.urls import path

from {{cookiecutter.project_slug}}.users import views

app_name = "users"
urlpatterns = [
    path("register/", views.registration_view, name="register"),
    path("login/", views.login_view, name="login"),
]
