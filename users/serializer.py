from rest_framework import serializers
from .models import User, Role


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
        role = attrs['role']
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'Username': 'This username is exists'}
            )
        if self.context['request'].user.role == Role.ASSISTANT:
            if role == Role.MANAGER or role == Role.ASSISTANT:
                raise serializers.ValidationError(
                    {'Permission': "You don't have permission"}
                )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UpdateInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class ChangePasswordSerializer(serializers.Serializer):
    user_password = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=20)
    new_password = serializers.CharField(max_length=50)

    def validate(self, attrs):
        user_password = attrs['user_password']
        username = attrs['username']
        up_user = self.context['request'].user
        if not up_user.check_password(user_password):
            raise serializers.ValidationError(
                {'Password': 'Your password is incorrect'}
            )
        low_user = User.objects.filter(username=username)
        if not low_user.exists():
            raise serializers.ValidationError(
                {'username': 'This username is not exists'}
            )
        if up_user.role == Role.ASSISTANT:
            if low_user.first().role == Role.MANAGER or low_user.first().role == Role.ASSISTANT:
                raise serializers.ValidationError(
                    {'Permission': "You don't have permission"}
                )
        return attrs

    def process(self, validated_data):
        username = validated_data['username']
        new_password = validated_data['new_password']
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()

    def save(self, **kwargs):
        self.process(self.validated_data)
