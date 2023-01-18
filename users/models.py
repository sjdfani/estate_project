from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from .manager import CustomUserManager


class Role(models.TextChoices):
    MANAGER = ('manager', 'Manager')
    ASSISTANT = ('assistant', 'Assistant')
    ADMIN = ('admin', 'Admin')
    ADVISER = ('adviser', 'Adviser')
    USER = ('user', 'User')
    NONE = ('none', 'None')


class User(AbstractBaseUser):
    username = models.CharField(
        max_length=20, unique=True, verbose_name='Username'
    )
    fullname = models.CharField(max_length=50, verbose_name='Fullname')
    phone = models.CharField(
        max_length=11, verbose_name='Phone Number', null=True, blank=True
    )
    address = models.TextField(verbose_name='Address', null=True, blank=True)
    role = models.CharField(
        max_length=9, choices=Role.choices, default=Role.NONE, verbose_name='Role'
    )
    date_joined = models.DateTimeField(default=timezone.now)
    access_codes = models.CharField(
        max_length=200, verbose_name='Access Codes', null=True, blank=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fullname', 'role']

    objects = CustomUserManager()

    def is_staff(self):
        return True

    def has_module_perms(self, kwargs):
        return True

    def has_perm(self, kwargs):
        return True

    def __str__(self):
        return self.username
