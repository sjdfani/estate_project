from rest_framework import serializers
from .models import Buy_Sell_Home


class HomeList(serializers.ModelSerializer):
    class Meta:
        model = Buy_Sell_Home
        fields = '__all__'
