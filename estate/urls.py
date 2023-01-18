from django.urls import path
from .views import (
    BS_Home_List, Create_BS_Home, Change_Status_BS_Home
)

app_name = 'estate'

urlpatterns = [
    path('list/', BS_Home_List.as_view(), name='home-list'),
    path('create-home/', Create_BS_Home.as_view(), name='create-home'),
    path('change-status/', Change_Status_BS_Home.as_view(), name='change-status'),
]
