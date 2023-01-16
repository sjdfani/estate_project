from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.utils import timezone
from .serializer import (
    LoginSerializer, UserSerializer, RegisterSerializer
)
from .models import User
from .utils import get_tokens_for_user
from .permission import Is_Manager


class Login(APIView):
    def post(self, request):
        login_status = None
        role = None
        serializer = LoginSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = User.objects.filter(username=username).first()
            if user:
                user_data = UserSerializer(user).data
                if user.is_manager:
                    if user.check_password(password):
                        role = 'manager'
                        login_status = True
                    else:
                        login_status = False
                elif user.is_admin:
                    if user.check_password(password):
                        role = 'admin'
                        login_status = True
                    else:
                        login_status = False
                elif user.is_adviser:
                    if user.check_password(password):
                        role = 'adviser'
                        login_status = True
                    else:
                        login_status = False
                elif user.is_user:
                    if user.check_password(password):
                        role = 'user'
                        login_status = True
                    else:
                        login_status = False
                if login_status:
                    user.last_login = timezone.now()
                    user.save()
                    message = {
                        'role': role,
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
    permission_classes = [Is_Manager]
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
