from difflib import IS_CHARACTER_JUNK
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


from django.contrib.auth.models import User
from django.contrib.auth.models import (
    AbstractUser,
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# class MyUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     username = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100, default="enter")
#     password = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)

#     address = models.CharField(max_length=100)


class CustomUserManager(BaseUserManager):
    def create_user(
        self, username, email, password, first_name, last_name, mobile, address
    ):
        if not email:
            raise ValueError("email required")
        if not password:
            raise ValueError("password required")
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            address=address,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, username, email, password, first_name, last_name, mobile, address
    ):
        if password is None:
            raise TypeError("Superuser must have a password")
        user = self.create_user(
            username,
            email,
            password,
            first_name,
            last_name,
            mobile,
            address,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


# create user model with extra field
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile = models.IntegerField()
    address = models.CharField(max_length=100)
    is_varified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = (
        "email"  # telling django user will login using email not by username
    )
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
        "mobile",
        "address",
    ]  # dont use email in required fields otherwise it will throw error because email is used as an username already

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    # genration of tokn after user creation
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
