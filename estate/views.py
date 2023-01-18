from rest_framework.generics import ListAPIView, CreateAPIView
from users.permission import Is_Any_Access_Except_Adviser
from users.models import Role
from .serializer import (
    HomeList,
)
from .models import Buy_Sell_Home


class Buy_Sell_Home_List(ListAPIView):
    permission_classes = [Is_Any_Access_Except_Adviser]
    serializer_class = HomeList

    def get_queryset(self):
        if self.request.user.role in [Role.MANAGER, Role.ASSISTANT]:
            return Buy_Sell_Home.objects.all()
        else:
            access_code = self.request.user.access_codes.split('-')
            return Buy_Sell_Home.objects.filter(area_code__in=access_code, status=True)


# class Create_Buy_Sell_Home(CreateAPIView):

#     serializer_class=
#     queryset =

#     def get_permissions(self):
#         return super().get_permissions()
