from django.urls import path
from .views import (
    Buy_Sell_Home_List,
)

app_name = 'estate'

urlpatterns = [
    path('list/', Buy_Sell_Home_List.as_view(), name='home-list'),
]
