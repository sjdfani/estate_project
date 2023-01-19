from rest_framework import serializers
from .models import User, Role, User_History
from .utils import return_persian_sentence


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
        up_user = self.context['request'].user
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        description = return_persian_sentence('create-user', up_user, user)
        User_History.objects.create(
            up_user=up_user, low_user=user, description=description)
        return user


class UpdateInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)

    def process(self, instance, validated_data):
        text = ''
        status = False
        for key, value in validated_data.items():
            if key == 'username':
                if instance.username != value:
                    status = True
                    text += f'{value} <- {instance.username} :شناسه\n'
            elif key == 'fullname':
                if instance.fullname != value:
                    status = True
                    text += f'{value} <- {instance.fullname} :نام کامل\n'
            elif key == 'phone':
                if instance.phone != value:
                    status = True
                    text += f'{value} <- {instance.phone} :تلفن\n'
            elif key == 'address':
                if instance.address != value:
                    status = True
                    text += f'{value} <- {instance.address} :آدرس\n'
            elif key == 'role':
                if instance.role != value:
                    status = True
                    text += f'{value} <- {instance.role} :نقش\n'
            elif key == 'access_codes':
                if instance.access_codes != value:
                    status = True
                    text += f'{value} <- {instance.access_codes} :سطح دسترسی\n'
        return text, status

    def update(self, instance, validated_data):
        up_user = self.context['request'].user
        user = User.objects.get(pk=instance.id)
        text, status = self.process(instance, validated_data)
        if status:
            description = return_persian_sentence('update-user', up_user, user)
            description += '\n'+text
            User_History.objects.create(
                up_user=up_user, low_user=user, description=description)
        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    user_password = serializers.CharField(max_length=50)
    user_id = serializers.IntegerField()
    new_password = serializers.CharField(max_length=50)

    def validate(self, attrs):
        user_password = attrs['user_password']
        user_id = attrs['user_id']
        up_user = self.context['request'].user
        if not up_user.check_password(user_password):
            raise serializers.ValidationError(
                {'Password': 'Your password is incorrect'}
            )
        low_user = User.objects.filter(pk=user_id)
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
        up_user = self.context['request'].user
        user_id = validated_data['user_id']
        new_password = validated_data['new_password']
        user = User.objects.get(pk=user_id)
        user.set_password(new_password)
        user.save()
        description = return_persian_sentence('change-password', up_user, user)
        User_History.objects.create(
            up_user=user, low_user=user, description=description)

    def save(self, **kwargs):
        self.process(self.validated_data)


class UserHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = User_History
        fields = '__all__'

    def to_representation(self, instance):
        request = self.context['request']
        res = super().to_representation(instance)
        res['up_user'] = UserSerializer(
            instance.up_user, context={'request': request}
        ).data
        res['low_user'] = UserSerializer(
            instance.low_user, context={'request': request}
        ).data
        return res


class UserHistorySerializerFields(serializers.ModelSerializer):
    class Meta:
        model = User_History
        fields = ('id', 'description')
