from rest_framework import mixins, viewsets, filters

from rest_framework.permissions import IsAuthenticated
from core.viewsets.mixins import AppModelViewSet
from core.viewsets.base import CoreAttributeViewSet

from django.db.models.query import QuerySet

from core.permissions.base import IsOwnerPermission, IsOwnerOrObjectPublicPermission

# from .serializers import UserSerializer, GroupSerializer, OwnerUserSerializer
from .models import KnowledgeBase
from .serializers import KnowledgeBaseSerializer
# from .filters import UserGroupFilter, StringUserStatusFilter, AdminStatusFilter


class KnowledgeBaseViewSet(
    AppModelViewSet
):

    queryset = KnowledgeBase.objects.all().order_by("-pk")
    serializer_class = KnowledgeBaseSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'title', 'description', 'owner__first_name', 'owner__last_name', "id"
    ]

    def get_queryset(self, *args, **kwargs):
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            if self.action == "partial_update" or self.action == "update" or self.action == "retrieve":
                queryset = queryset.all()
            elif self.action == "list":
                queryset = queryset.filter(is_public=True)
            else:
                queryset = queryset.filter(is_public=True)

        return queryset

    def get_permissions(self):
        if self.action == "partial_update" or self.action == "update":
            return [permission() for permission in [IsAuthenticated, IsOwnerPermission]]
        elif self.action == "retrieve":
            return [permission() for permission in [IsAuthenticated, IsOwnerOrObjectPublicPermission]]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
