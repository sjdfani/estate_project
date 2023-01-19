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
        user = self.context['request'].user
        home = Buy_Sell_Home.objects.create(creator=user, **validated_data)
        Home_History.objects.create(
            user=user, home=home, title='create-home', descriptions='create home')
        return home


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
        user = self.context['request'].user
        home = Buy_Sell_Home.objects.get(pk=home_id)
        state = None
        if status:
            home.status = True
            home.is_archived = False
            state = 1
        else:
            home.status = False
            home.is_archived = True
            state = 2
        home.checked_by = self.context['request'].user
        home.checked_date = timezone.now()
        home.save()
        if state == 1:
            Home_History.objects.create(
                user=user, home=home, title='change-status', descriptions='accepted')
        elif state == 2:
            Home_History.objects.create(
                user=user, home=home, title='change-status', descriptions='rejected')

    def save(self, **kwargs):
        self.process(self.validated_data)


class Restore_Archived_BS_Home_Serializer(serializers.Serializer):
    home = serializers.IntegerField()

    def validate_home(self, value):
        if not Buy_Sell_Home.objects.filter(pk=value).exists():
            raise serializers.ValidationError('This home is not exists')
        return value

    def process(self, validated_data):
        user = self.context['request'].user
        home_id = validated_data['home']
        home = Buy_Sell_Home.objects.get(pk=home_id)
        home.status = False
        home.is_archived = False
        home.save()
        Home_History.objects.create(
            user=user, home=home, title='restore-archived-home', descriptions='Restore archived home complete')

    def save(self, **kwargs):
        self.process(self.validated_data)


class Update_BS_Home_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Buy_Sell_Home
        exclude = (
            'checked_by', 'checked_date', 'creator', 'is_archived', 'status'
        )

    def process(self, instance, validated_data):
        text = ''
        status = False
        for key, value in validated_data.items():
            if key == 'area_code':
                if instance.area_code != value:
                    status = True
                    text += f'area_code:\n{value} <- {instance.area_code}\n'
            elif key == 'owner_name':
                if instance.owner_name != value:
                    status = True
                    text += f'owner_name:\n{value} <- {instance.owner_name}\n'
            elif key == 'owner_phone':
                if instance.owner_phone != value:
                    status = True
                    text += f'owner_phone:\n{value} <- {instance.owner_phone}\n'
            elif key == 'street':
                if instance.street != value:
                    status = True
                    text += f'street:\n{value} <- {instance.street}\n'
            elif key == 'plaque':
                if instance.plaque != value:
                    status = True
                    text += f'plaque:\n{value} <- {instance.plaque}\n'
            elif key == 'floors':
                if instance.floors != value:
                    status = True
                    text += f'floors:\n{value} <- {instance.floors}\n'
            elif key == 'meterage':
                if instance.meterage != value:
                    status = True
                    text += f'meterage:\n{value} <- {instance.meterage}\n'
            elif key == 'price_per_meter':
                if instance.price_per_meter != value:
                    status = True
                    text += f'price_per_meter:\n{value} <- {instance.price_per_meter}\n'
            elif key == 'total_price':
                if instance.total_price != value:
                    status = True
                    text += f'total_price:\n{value} <- {instance.total_price}\n'
            elif key == 'customer_name':
                if instance.customer_name != value:
                    status = True
                    text += f'customer_name:\n{value} <- {instance.customer_name}\n'
            elif key == 'style':
                if instance.style != value:
                    status = True
                    text += f'style:\n{value} <- {instance.style}\n'
            elif key == 'heating':
                if instance.heating != value:
                    status = True
                    text += f'heating:\n{value} <- {instance.heating}\n'
            elif key == 'bottom':
                if instance.bottom != value:
                    status = True
                    text += f'bottom:\n{value} <- {instance.bottom}\n'
            elif key == 'electricity':
                if instance.electricity != value:
                    status = True
                    text += f'electricity:\n{value} <- {instance.electricity}\n'
            elif key == 'kitchen':
                if instance.kitchen != value:
                    status = True
                    text += f'kitchen:\n{value} <- {instance.kitchen}\n'
            elif key == 'faucets':
                if instance.faucets != value:
                    status = True
                    text += f'faucets:\n{value} <- {instance.faucets}\n'
            elif key == 'bathtub':
                if instance.bathtub != value:
                    status = True
                    text += f'bathtub:\n{value} <- {instance.bathtub}\n'
            elif key == 'window':
                if instance.window != value:
                    status = True
                    text += f'window:\n{value} <- {instance.window}\n'
            elif key == 'description':
                if instance.description != value:
                    status = True
                    text += f'description:\n{value} <- {instance.description}\n'
        return text, status

    def update(self, instance, validated_data):
        user = self.context['request'].user
        home = Buy_Sell_Home.objects.get(pk=instance.id)
        text, status = self.process(instance, validated_data)
        if status:
            Home_History.objects.create(
                user=user, home=home, title='update-home', descriptions=text)
        return super().update(instance, validated_data)


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
        user = self.context['request'].user
        home = Buy_Sell_Home.objects.get(pk=home_id)
        home.description = description
        home.save()
        Home_History.objects.create(
            user=user, home=home, title='set-description-home', descriptions=description)

    def save(self, **kwargs):
        self.process(self.validated_data)


class Home_History_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Home_History
        fields = '__all__'


class Home_History_Serializer_Fields(serializers.ModelSerializer):
    class Meta:
        model = Home_History
        fields = ('id', 'title', 'descriptions')
