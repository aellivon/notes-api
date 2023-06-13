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
        # 'OPTIONS': view_permissions,
        # 'HEAD': view_permissions,
        'POST': permissions.DjangoModelPermissions.perms_map['POST'],
        'PUT': permissions.DjangoModelPermissions.perms_map['PUT'],
        'PATCH': permissions.DjangoModelPermissions.perms_map['PATCH'],
        'DELETE': permissions.DjangoModelPermissions.perms_map['DELETE'],
    }

    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True

        return super().has_permission(request, view)
