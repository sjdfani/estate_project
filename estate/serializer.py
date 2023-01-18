from rest_framework import serializers
from django.utils import timezone
from .models import Buy_Sell_Home


class HomeSerializer(serializers.ModelSerializer):
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
    home = serializers.IntegerField()
    status = serializers.BooleanField()

    def validate_home(self, value):
        if not Buy_Sell_Home.objects.filter(pk=value).exists():
            raise serializers.ValidationError('This home is not exists')
        return value

    def process(self, validated_data):
        home_id = validated_data['home']
        status = validated_data['status']
        home = Buy_Sell_Home.objects.get(pk=home_id)
        if status:
            home.status = True
            home.is_archived = False
        else:
            home.status = False
            home.is_archived = True
        home.checked_by = self.context['request'].user
        home.checked_date = timezone.now()
        home.save()

    def save(self, **kwargs):
        self.process(self.validated_data)


class Update_BS_Home_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Buy_Sell_Home
        exclude = (
            'checked_by', 'checked_date', 'creator', 'is_archived', 'status'
        )
