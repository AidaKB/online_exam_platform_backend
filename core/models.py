from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from . import consts
from .managers import CustomUserManager


class CustomUser(AbstractUser, PermissionsMixin):
    user_type = models.CharField(max_length=20, choices=consts.USER_TYPE_CHOICES, default="admin",
                                 verbose_name="نوع کاربر")
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_team = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'
    objects = CustomUserManager()

    def __str__(self):
        return self.username
