from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import Role
from users.permission import (
    Is_Any_Access_Except_Advisor, Is_Manager_OR_Assistant_OR_Advisor, Is_Manager_OR_Assistant_OR_Admin,
    Is_Admin, Is_Manager_OR_Assistant
)
from .serializer import (
    HomeSerializer, Create_BS_Home_Serializer, Change_Status_BS_Home_Serializer,
    Update_BS_Home_Serializer, Set_Description_BS_Home_Serializer
)
from .models import Buy_Sell_Home


class BS_Home_List(ListAPIView):
    permission_classes = [Is_Any_Access_Except_Advisor]
    serializer_class = HomeSerializer

    def get_queryset(self):
        if self.request.user.role in [Role.MANAGER, Role.ASSISTANT]:
            return Buy_Sell_Home.objects.all()
        else:
            access_code = self.request.user.access_codes
            if access_code:
                access_code = access_code.split('-')
                return Buy_Sell_Home.objects.filter(area_code__in=access_code, status=True)
            else:
                return []


class Create_BS_Home(CreateAPIView):
    permission_classes = [Is_Manager_OR_Assistant_OR_Advisor]
    serializer_class = Create_BS_Home_Serializer
    queryset = Buy_Sell_Home.objects.all()


class Change_Status_BS_Home(APIView):
    permission_classes = [Is_Manager_OR_Assistant_OR_Admin]

    def post(self, request):
        serializer = Change_Status_BS_Home_Serializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = {'change-status': 'Change status complete'}
            return Response(message, status=status.HTTP_200_OK)


class UnChecked_BS_Home_List(ListAPIView):
    permission_classes = [Is_Admin]
    serializer_class = HomeSerializer

    def get_queryset(self):
        access_code = self.request.user.access_codes
        if access_code:
            access_code = access_code.split('-')
            return Buy_Sell_Home.objects.filter(area_code__in=access_code, status=False, is_archived=False)
        else:
            return []


class Archived_BS_Home(ListAPIView):
    permission_classes = [Is_Manager_OR_Assistant]
    serializer_class = HomeSerializer
    queryset = Buy_Sell_Home.objects.filter(is_archived=True)


class Update_BS_Home(RetrieveUpdateDestroyAPIView):
    permission_classes = [Is_Manager_OR_Assistant]
    queryset = Buy_Sell_Home.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return HomeSerializer
        return Update_BS_Home_Serializer


class Set_Description_BS_Home(APIView):
    def post(self, request):
        serializer = Set_Description_BS_Home_Serializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = {'set-description': 'Set description complete'}
            return Response(message, status=status.HTTP_200_OK)
