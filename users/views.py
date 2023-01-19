from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from django.utils import timezone
from .serializer import (
    LoginSerializer, UserSerializer, RegisterSerializer, UpdateInformationSerializer,
    ChangePasswordSerializer, UserHistorySerializer
)
from .models import User, Role, User_History
from .utils import get_tokens_for_user
from .permission import Is_Manager_OR_Assistant


class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = User.objects.filter(username=username).first()
            if user:
                if user.check_password(password):
                    user.last_login = timezone.now()
                    user.save()
                    user_data = UserSerializer(user).data
                    message = {
                        'user': user_data,
                        'tokens': get_tokens_for_user(user)
                    }
                    return Response(message, status=status.HTTP_200_OK)
                else:
                    message = {'password': 'Password is incorrect'}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
            else:
                message = {'message': 'User not found'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)


class Register(CreateAPIView):
    permission_classes = [Is_Manager_OR_Assistant]
    serializer_class = RegisterSerializer
    queryset = User.objects.all()


class UserList(ListAPIView):
    permission_classes = [Is_Manager_OR_Assistant]
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.role == Role.ASSISTANT:
            return User.objects.exclude(role=Role.MANAGER).exclude(role=Role.ASSISTANT)
        return User.objects.all()


class UpdateInformation(RetrieveUpdateDestroyAPIView):
    permission_classes = [Is_Manager_OR_Assistant]
    serializer_class = UpdateInformationSerializer

    def get_queryset(self):
        if self.request.user.role == Role.ASSISTANT:
            return User.objects.exclude(role=Role.MANAGER).exclude(role=Role.ASSISTANT)
        return User.objects.all()


class ChangePassword(APIView):
    permission_classes = [Is_Manager_OR_Assistant]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = {'change-password': 'change password complete'}
            return Response(message, status=status.HTTP_200_OK)


class UserHistoryList(ListAPIView):
    permission_classes = [Is_Manager_OR_Assistant]
    serializer_class = UserHistorySerializer

    def get_queryset(self):
        if self.request.user.role == Role.ASSISTANT:
            return User_History.objects.exclude(up_user__role=Role.MANAGER)
        return User_History.objects.all()


class UserHistoryPerUser(ListAPIView):
    permission_classes = [Is_Manager_OR_Assistant]
    serializer_class = UserHistorySerializer

    def get_queryset(self):
        user = self.request.user
        return User_History.objects.filter(up_user=user)
