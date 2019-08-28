from django.contrib.auth import get_user_model, forms

User = get_user_model()


class UserCreationForm(forms.UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")
