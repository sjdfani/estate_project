from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from django.utils import timezone
from django.db.models import Q
from .serializer import (
    LoginSerializer, UserSerializer, RegisterSerializer, UpdateInformationSerializer,
    ChangePasswordSerializer,
)
from .models import User, Role
from .utils import get_tokens_for_user
from .permission import Is_Manager, Is_Assistant


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
                user_data = UserSerializer(user).data
                if user.check_password(password):
                    user.last_login = timezone.now()
                    user.save()
                    message = {
                        'role': user.role,
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
    permission_classes = [Is_Manager, Is_Assistant]
    serializer_class = RegisterSerializer
    queryset = User.objects.all()


class UserList(ListAPIView):
    permission_classes = [Is_Manager, Is_Assistant]
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.role == Role.ASSISTANT:
            lookup = ~Q(role=Role.ASSISTANT, role=Role.MANAGER)
            return User.objects.filter(lookup)
        return User.objects.all()


class UpdateInformation(RetrieveUpdateDestroyAPIView):
    permission_classes = [Is_Manager, Is_Assistant]
    serializer_class = UpdateInformationSerializer

    def get_queryset(self):
        if self.request.user.role == Role.ASSISTANT:
            lookup = ~Q(role=Role.ASSISTANT, role=Role.MANAGER)
            return User.objects.filter(lookup)
        return User.objects.all()


class ChangePassword(APIView):
    permission_classes = [Is_Manager, Is_Assistant]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = {'change-password': 'change password complete'}
            return Response(message, status=status.HTTP_200_OK)
