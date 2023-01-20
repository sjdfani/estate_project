from django.urls import path
from .views import (
    Login, Register, UserList, UpdateInformation, ChangePassword, UserHistoryList,
    UserHistoryPerUser
)

app_name = 'users'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('list/', UserList.as_view(), name='user-list'),
    path('list/<int:pk>/', UpdateInformation.as_view(), name='update-info'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
    path('user-history-list/<int:pk>/',
         UserHistoryList.as_view(), name='list-user-history'),
    path('user-history/', UserHistoryPerUser.as_view(), name='user-history'),
]
