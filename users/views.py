from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
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
        return User.objects.exclude(role=Role.MANAGER)


class UpdateInformation(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateInformationSerializer

    def delete(self, request, *args, **kwargs):
        low_user_id = self.kwargs['pk']
        user = User.objects.get(pk=low_user_id)
        User_History.objects.create(
            up_user=request.user, low_user=user, title='delete-user', description='delete user successful')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.role == Role.ASSISTANT:
            return User.objects.exclude(role=Role.MANAGER).exclude(role=Role.ASSISTANT)
        return User.objects.all()


class Get_User_Data(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return User.objects.filter(pk=user_id)


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
        user_id = self.kwargs['pk']
        user = User.objects.get(pk=user_id)
        return User_History.objects.filter(low_user=user)


class UserHistoryPerUser(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserHistorySerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.MANAGER:
            return User_History.objects.filter(up_user=user).order_by('-pk')
        return User_History.objects.filter(low_user=user).order_by('-pk')
