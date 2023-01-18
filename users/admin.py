from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'fullname', 'phone', 'role', 'date_joined')
    list_filter = ('role',)
    fieldsets = (
        (_('Personal information'), {
            'fields': ('username', 'fullname', 'phone', 'address')
        }),
        (_('Date information'), {
            'fields': ('date_joined', 'last_login')
        }),
        (_('Permission options'), {
            'fields': ('role', 'access_codes')
        })
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'fullname', 'role')}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    groups = []
    filter_horizontal = ()
    filter_vertical = ()


admin.site.register(User, CustomUserAdmin)
