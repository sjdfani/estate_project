from rest_framework_simplejwt.tokens import RefreshToken
from .models import User_History


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def return_persian_sentence(type, up_user, low_user):
    if type == 'create-user':
        description = f'در سامانه ایجاد شد {up_user.username} توسط {low_user.username} کاربر با شناسه'
        return description
    elif type == 'change-password':
        description = f'در سامانه تغییر کرد {up_user.username} توسط {low_user.username} رمز کاربر با شناسه'
        return description
    elif type == 'update-user':
        description = f'در سامانه تغییر کرد {up_user.username} توسط {low_user.username} اطلاعات کاربر با شناسه'
        return description
