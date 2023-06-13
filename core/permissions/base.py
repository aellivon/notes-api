from rest_framework import permissions


class RestBasePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.has_perm(
            (f"{view.get_queryset().model._meta.app_label}"
             f".{view.get_queryset().model.__name__.lower()}.rest_{view.action}")
        ):
            return True
        return False


class DjangoCoreModelPermissions(permissions.DjangoModelPermissions):
    view_permissions = ['%(app_label)s.view_%(model_name)s']

    perms_map = {
        'GET': view_permissions,
        'OPTIONS': [],
        'HEAD': [],
        'POST': permissions.DjangoModelPermissions.perms_map['POST'],
        'PUT': permissions.DjangoModelPermissions.perms_map['PUT'],
        'PATCH': permissions.DjangoModelPermissions.perms_map['PATCH'],
        'DELETE': permissions.DjangoModelPermissions.perms_map['DELETE'],
    }

    def has_permission(self, request, view, delay_decision=False, from_object_permission=False):

        if request.user.is_superuser:
            return True

        return super().has_permission(request, view)


class IsOwnerPermission(permissions.BasePermission):

    def _queryset(self, view):
        assert hasattr(view, 'get_queryset') \
            or getattr(view, 'queryset', None) is not None, (
            'Cannot apply {} on a view that does not set '
            '`.queryset` or have a `.get_queryset()` method.'
        ).format(self.__class__.__name__)

        if hasattr(view, 'get_queryset'):
            queryset = view.get_queryset()
            assert queryset is not None, (
                '{}.get_queryset() returned None'.format(view.__class__.__name__)
            )
            return queryset
        return view.queryset

    def has_object_permission(self, request, view, obj):
        queryset = self._queryset(view)
        if queryset.model._meta.model_name == "user":
            if request.user.pk == obj.pk:
                return True
        return False
