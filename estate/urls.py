from django.urls import path
from .views import (
    Buy_Sell_Home_List, Create_Buy_Sell_Home
)

app_name = 'estate'

urlpatterns = [
    path('list/', Buy_Sell_Home_List.as_view(), name='home-list'),
    path('create-home/', Create_Buy_Sell_Home.as_view(), name='create-home')
]
