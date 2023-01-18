from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import Role
from users.permission import (
    Is_Any_Access_Except_Adviser, Is_Manager_OR_Assistant_OR_Adviser
)
from .serializer import (
    HomeList, Create_BS_Home_Serializer, Change_Status_BS_Home_Serializer
)
from .models import Buy_Sell_Home


class BS_Home_List(ListAPIView):
    permission_classes = [Is_Any_Access_Except_Adviser]
    serializer_class = HomeList

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
    permission_classes = [Is_Manager_OR_Assistant_OR_Adviser]
    serializer_class = Create_BS_Home_Serializer
    queryset = Buy_Sell_Home.objects.all()


class Change_Status_BS_Home(APIView):
    def post(self, request):
        serializer = Change_Status_BS_Home_Serializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = {'change-status': 'Change status complete'}
            return Response(message, status=status.HTTP_200_OK)


class UnChecked_BS_Home_List(APIView):
    pass
