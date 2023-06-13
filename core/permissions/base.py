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

    def has_permission(self, request, view, delay_decision=False, from_object_permission=False):

        if request.user.is_superuser:
            return True
        if request.method == "PATCH" and not from_object_permission:
            # We need to check if the object is the logged in user or not
            delay_decision = True

        if from_object_permission:
            delay_decision = False

        if not delay_decision:
            return super().has_permission(request, view)
        else:
            return True

    def has_object_permission(self, request, view, obj):
        queryset = self._queryset(view)
        if queryset.model._meta.model_name == "user":
            if request.user.pk == obj.pk:
                return True

        return self.has_permission(request, view, delay_decision=False, from_object_permission=True)
