from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, first_name=None, last_name=None, **extra_fields):
        if username is None:
            raise ValueError('Users must have a username')
        if password is None:
            raise ValueError('Users must have a password')
        if first_name is None:
            raise ValueError('Users must have a first name')
        if last_name is None:
            raise ValueError('Users must have a last name')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, username, password, first_name=None, last_name=None, **extra_fields):
        user = self.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_superuser=True,
            is_staff=True,
            **extra_fields
        )
        user.save()
        return user
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username
    objects = UserManager()

    def tokens(self):
        refresh_token = RefreshToken.for_user(self)
        return {'refresh': str(refresh_token), 'access': str(refresh_token.access_token)}