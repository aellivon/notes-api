from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, filters

from core.permissions.base import DjangoCoreModelPermissions, IsOwnerPermission

from .serializers import UserSerializer, GroupSerializer
from .models import Group
from .filters import UserGroupFilter, StringUserStatusFilter, AdminStatusFilter


class UserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    queryset = get_user_model().objects.all().order_by("-pk")
    serializer_class = UserSerializer
    permission_classes = [DjangoCoreModelPermissions]
    http_method_names = ['get', 'post', 'patch']
    filter_backends = [filters.SearchFilter, UserGroupFilter, StringUserStatusFilter, AdminStatusFilter]
    search_fields = [
        'first_name', 'last_name', 'email', 'furigana_fname', 'furigana_lname',
        'position', "id"
    ]

    def get_permissions(self):
        if self.action == "partial_update" or self.action == "update":
            return [permission() for permission in [DjangoCoreModelPermissions | IsOwnerPermission]]
        return super().get_permissions()


class GroupViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Group.objects.all().order_by('-pk')
    serializer_class = GroupSerializer
    permission_classes = [DjangoCoreModelPermissions]
    filter_backends = []
    search_fields = [
        'name', "id"
    ]
