from django.urls import path
from .views import (
    BS_Home_List, Create_BS_Home, Change_Status_BS_Home, UnChecked_BS_Home_List,
    Archived_BS_Home, Update_BS_Home, Set_Description_BS_Home
)

app_name = 'estate'

urlpatterns = [
    path('list/', BS_Home_List.as_view(), name='home-list'),
    path('list/<int:pk>/', Update_BS_Home.as_view(), name='update-home'),
    path('create-home/', Create_BS_Home.as_view(), name='create-home'),
    path('change-status/', Change_Status_BS_Home.as_view(), name='change-status'),
    path('unchecked-home/', UnChecked_BS_Home_List.as_view(), name='unchecked-list'),
    path('archived-home/', Archived_BS_Home.as_view(), name='archived-home'),
    path('set-description/', Set_Description_BS_Home.as_view(),
         name='set-description'),
]
