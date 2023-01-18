from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from .models import Role


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_('The Username must be set'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('role', Role.MANAGER)

        if extra_fields.get('role') == 'manager':
            raise ValueError(_('Manager must have role=manager.'))
        return self.create_user(username, password, **extra_fields)
