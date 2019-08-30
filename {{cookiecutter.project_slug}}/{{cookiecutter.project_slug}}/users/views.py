import logging

import pytz
from django.contrib.auth import authenticate, get_user_model, password_validation
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from {{cookiecutter.project_slug}}.users.services import user as user_service

log = logging.getLogger(__name__)

User = get_user_model()


class EmptySerializer(serializers.Serializer):
    pass


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    timezone = serializers.CharField(required=False)

    default_error_messages = {
        "cannot_create_user": "Unable to create account.",
        "wrong_timezone": "This timezone does not exist.",
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD,
            User._meta.pk.name,
            "password",
            "timezone",
        )

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def validate_timezone(self, value):
        if value in pytz.all_timezones:
            return value
        self.fail("wrong_timezone")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email")


class RegistrationView(generics.GenericAPIView):
    """
    Use this endpoint to register new user.
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: EmptySerializer()})
    def post(self, request):
        serialized_data = self.get_serializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        data = serialized_data.validated_data

        user_service.create(data)

        return Response({}, status.HTTP_201_CREATED)


registration_view = RegistrationView.as_view()


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    default_error_messages = {
        "wrong_email_or_password": "Wrong email or password",
        "user_not_active": "This account is not activated",
    }

    def validate(self, attrs):
        user = authenticate(
            self.context["request"], email=attrs["email"], password=attrs["password"]
        )
        if not user:
            self.fail("wrong_email_or_password")
        if not user.is_active:
            self.fail("user_not_active")
        return attrs


class JWTSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class ResponseLoginSerializer(serializers.Serializer):
    jwt_token = JWTSerializer()
    user = UserSerializer()


class LoginView(generics.GenericAPIView):
    """
    Use this endpoint to login a user.
    """

    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ResponseLoginSerializer()})
    def post(self, request):
        serialized_data = LoginSerializer(data=request.data, context={"request": request})
        serialized_data.is_valid(raise_exception=True)
        data = serialized_data.validated_data

        user = user_service.get(data["email"])

        refresh_token = RefreshToken.for_user(user)
        serialized_data = ResponseLoginSerializer(
            data={
                "jwt_token": JWTSerializer(
                    data={"refresh": str(refresh_token), "access": str(refresh_token.access_token)}
                ).initial_data,
                "user": UserSerializer(user).data,
            }
        )
        return Response(serialized_data.initial_data, status.HTTP_200_OK)


login_view = LoginView.as_view()
