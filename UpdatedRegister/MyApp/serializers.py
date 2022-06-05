from lib2to3.pgen2.tokenize import TokenError
from typing_extensions import Required
import django

# from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

# from django.contrib.auth.models import User
from .models import User
from django.contrib import auth
from django.contrib.auth.password_validation import validate_password


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "address",
            "first_name",
            "last_name",
            "mobile",
        ]

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        address = attrs.get("address")
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")
        mobile = attrs.get("mobile")

        return attrs

    # create user
    def create(self, validate_data):

        user = User.objects.create_user(**validate_data)

        return user


# login user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=100,
    )

    password = serializers.CharField(max_length=100, write_only=True)

    username = serializers.CharField(max_length=100, read_only=True)

    tokens = serializers.CharField(max_length=100, read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "tokens", "username"]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # now authenticate the credentials
        user = auth.authenticate(
            email=email, password=password
        )  # check user is authenticated or not
        # print(user.is_authenticated, "authenticated")
        # print(user.is_anonymous, "anonymous")
        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        # now check if user exists
        print(user.id, "user id")
        if not user:
            raise serializers.ValidationError("user is not exist")
        if not user.is_active:
            raise serializers.ValidationError("user is not active")

        # print({"email": user.email, "username": user.username, "token": user.tokens()})
        print(user.tokens()["refresh"], "refresh")

        return {"email": user.email, "username": user.username, "tokens": user.tokens}


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {"invalid_token": "token is expired"}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        print(self.token)
        return attrs

    def save(self, **kwargs):
        try:
            refresh_token = RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail("invalid token")


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=100,
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    new_pass1 = serializers.CharField(max_length=100, write_only=True, required=True)
    new_pass2 = serializers.CharField(max_length=100, write_only=True, required=True)

    class Meta:
        model = User
        fields = ("password", "new_pass1", "new_pass2")

    def validate(self, attrs):
        password = attrs["password"]
        new_pass1 = attrs["new_pass1"]
        new_pass2 = attrs["new_pass2"]

        if new_pass1 != new_pass2:
            raise serializers.ValidationError("new passwords not match")

        return attrs

    def validate_password(self, value):
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError("old password is not correct")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_pass1"])
        instance.save()
        return instance
