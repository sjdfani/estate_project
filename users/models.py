from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from .manager import CustomUserManager


class User(AbstractBaseUser):
    username = models.CharField(
        max_length=20, unique=True, verbose_name='Username'
    )
    fullname = models.CharField(max_length=50, verbose_name='Fullname')
    phone = models.CharField(
        max_length=11, verbose_name='Phone Number', null=True, blank=True
    )
    address = models.TextField(verbose_name='Address', null=True, blank=True)
    is_manager = models.BooleanField(default=False, verbose_name='Is Manager')
    is_admin = models.BooleanField(default=False, verbose_name='Is Admin')
    is_adviser = models.BooleanField(default=False, verbose_name='Is Adviser')
    is_user = models.BooleanField(default=False, verbose_name='Is User')
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
