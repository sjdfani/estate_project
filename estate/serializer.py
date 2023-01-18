from rest_framework import serializers
from .models import Buy_Sell_Home


class HomeList(serializers.ModelSerializer):
    class Meta:
        model = Buy_Sell_Home
        fields = '__all__'


class Create_Buy_Sell_Home_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Buy_Sell_Home
        fields = '__all__'

    def create(self, validated_data):
        creator_user = self.context['request'].user
        home = Buy_Sell_Home.objects.create(
            creator=creator_user, **validated_data)
        return home

    def to_representation(self, instance):
        return super().to_representation(instance)
