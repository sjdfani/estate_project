from rest_framework.generics import ListAPIView, CreateAPIView
from users.permission import (
    Is_Any_Access_Except_Adviser, Is_Manager_OR_Assistant_OR_Adviser
)
from users.models import Role
from .serializer import (
    HomeList, Create_Buy_Sell_Home_Serializer
)
from .models import Buy_Sell_Home


class Buy_Sell_Home_List(ListAPIView):
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


class Create_Buy_Sell_Home(CreateAPIView):
    permission_classes = [Is_Manager_OR_Assistant_OR_Adviser]
    serializer_class = Create_Buy_Sell_Home_Serializer
    queryset = Buy_Sell_Home.objects.all()
