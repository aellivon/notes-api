from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, filters

from core.permissions.base import DjangoCoreModelPermissions, IsOwnerUserModelPermission
from core.viewsets.mixins import AppModelViewSet
from core.viewsets.base import CoreAttributeViewSet

from .serializers import UserSerializer, GroupSerializer, OwnerUserSerializer
from .models import Group
from .filters import UserGroupFilter, StringUserStatusFilter, AdminStatusFilter


class UserViewSet(
    CoreAttributeViewSet, AppModelViewSet
):
    queryset = get_user_model().objects.all().order_by("-pk")
    serializer_class = UserSerializer
    permission_classes = [DjangoCoreModelPermissions]
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [filters.SearchFilter, UserGroupFilter, StringUserStatusFilter, AdminStatusFilter]
    search_fields = [
        'first_name', 'last_name', 'email', 'furigana_fname', 'furigana_lname',
        'position', "id"
    ]

    def owner_and_no_permissions(self, *args, **kwargs):
        if not self.logged_in_user_has_privelege and self.logged_in_user_is_owner:
            return True
        return False

    def get_serializer(self, *args, **kwargs):
        if self.owner_and_no_permissions():
            self.serializer_class = OwnerUserSerializer
        return super().get_serializer(*args, **kwargs)

    def get_permissions(self):
        if self.action == "partial_update" or self.action == "update":
            return [permission() for permission in [DjangoCoreModelPermissions | IsOwnerUserModelPermission]]
        return super().get_permissions()


class GroupViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Group.objects.all().order_by('-pk')
    serializer_class = GroupSerializer
    permission_classes = [DjangoCoreModelPermissions]
    filter_backends = []
    search_fields = [
        'name', "id"
    ]
