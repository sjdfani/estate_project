from django.urls import path
from .views import (
    Login, Register, UserList, UpdateInformation, ChangePassword
)

app_name = 'users'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('list/', UserList.as_view(), name='user-list'),
    path('list/<int:pk>/', UpdateInformation.as_view(), name='update-info'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
]
