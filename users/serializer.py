from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=50)

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is not exists.')
        return value


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        username = attrs['username']
        permissions = [
            attrs['is_manager'], attrs['is_admin'],
            attrs['is_adviser'], attrs['is_user'],
        ]
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'username': 'This username is exists'}
            )
        if permissions.count(True) >= 2:
            raise serializers.ValidationError(
                {'role': 'You can choose one role'}
            )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UpdateInformationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class ChangePasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    new_password = serializers.CharField(max_length=50)

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            return serializers.ValidationError('This username is not exists')
        return value

    def process(self, validated_data):
        username = validated_data['username']
        new_password = validated_data['new_password']
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()

    def save(self, **kwargs):
        self.process(self.validated_data)
