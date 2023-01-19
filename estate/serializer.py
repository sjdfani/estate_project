from rest_framework import serializers
from django.utils import timezone
from .models import Buy_Sell_Home, Home_History
from users.serializer import UserSerializer


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


class Restore_Archived_BS_Home_Serializer(serializers.Serializer):
    home = serializers.IntegerField()

    def validate_home(self, value):
        if not Buy_Sell_Home.objects.filter(pk=value).exists():
            raise serializers.ValidationError('This home is not exists')
        return value

    def process(self, validated_data):
        home_id = validated_data['home']
        home = Buy_Sell_Home.objects.get(pk=home_id)
        home.status = False
        home.is_archived = False
        home.save()

    def save(self, **kwargs):
        self.process(self.validated_data)


class Update_BS_Home_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Buy_Sell_Home
        exclude = (
            'checked_by', 'checked_date', 'creator', 'is_archived', 'status'
        )


class Set_Description_BS_Home_Serializer(serializers.Serializer):
    home = serializers.IntegerField()
    description = serializers.CharField(max_length=200)

    def validate_home(self, value):
        if not Buy_Sell_Home.objects.filter(pk=value).exists():
            raise serializers.ValidationError('This home is not exists')
        return value

    def process(self, validated_data):
        home_id = validated_data['home']
        description = validated_data['description']
        home = Buy_Sell_Home.objects.get(pk=home_id)
        home.description = description
        home.save()

    def save(self, **kwargs):
        self.process(self.validated_data)


class Home_History_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Home_History
        fields = '__all__'

    def to_representation(self, instance):
        request = self.context['request']
        res = super().to_representation(instance)
        res['home'] = HomeSerializer(
            instance.home, context={'request': request}
        ).data
        res['user'] = UserSerializer(
            instance.user, context={'request': request}
        ).data
        return res


class Home_History_Serializer_Fields(serializers.ModelSerializer):
    class Meta:
        model = Home_History
        fields = ('id', 'title', 'description')
