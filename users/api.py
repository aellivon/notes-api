from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, filters

from core.permissions import RestBasePermission

from .serializers import UserSerializer, DivisionSerializer
from .models import Division
from .filters import UserDivisionFilter


class UserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [RestBasePermission]
    filter_backends = [filters.SearchFilter, UserDivisionFilter]
    search_fields = [
        'first_name', 'last_name', 'email', 'furigana_fname', 'furigana_lname',
        'position', "id"
    ]


class DivisionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Division.objects.all().order_by('pk')
    serializer_class = DivisionSerializer
    permission_classes = [RestBasePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'name', "id"
    ]


# class TypeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
#     queryset = Division.objects.all()
#     serializer_class = DivisionSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = [
#         'name', "id"
#     ]
