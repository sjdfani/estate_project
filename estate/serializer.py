from rest_framework import serializers
from .models import Buy_Sell_Home


class HomeList(serializers.ModelSerializer):
    class Meta:
        model = Buy_Sell_Home
        fields = '__all__'


class Create_BS_Home_Serializer(serializers.ModelSerializer):
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


class Change_Status_BS_Home_Serializer(serializers.Serializer):
    home_id = serializers.PrimaryKeyRelatedField(
        queryset=Buy_Sell_Home.objects.all()
    )
    status = serializers.BooleanField()

    def process(self, validated_data):
        home = validated_data['home_id']
        status = validated_data['status']
        if status:
            home.status = True
            home.is_archived = False
        else:
            home.status = False
            home.is_archived = True
        home.save()

    def save(self, **kwargs):
        self.process(self.validated_data)
