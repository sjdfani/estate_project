from django.urls import path
from .views import (
    BS_Home_List, Create_BS_Home, Change_Status_BS_Home, UnChecked_BS_Home_List,
    Archived_BS_Home, Update_BS_Home, Set_Description_BS_Home, Restore_Archived_BS_Home,
    Home_History_List, Home_History_Per_User, Home_History_Retrieve, Import_Excel_Data
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
    path('restore-archived-home/', Restore_Archived_BS_Home.as_view(),
         name='restore-archived-home'),
    path('list-home-history/', Home_History_List.as_view(),
         name='list-home-history'),
    path('home-history/', Home_History_Per_User.as_view(),
         name='home-history-per-user'),
    path('home-history/<int:pk>', Home_History_Retrieve.as_view(),
         name='home-history-retrieve'),
    path('import-excel/', Import_Excel_Data.as_view(), name='import-excel'),
]
