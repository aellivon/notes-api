from rest_framework import permissions


class RestBasePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.has_perm(
            f"{view.get_queryset().model._meta.app_label}.{view.get_queryset().model.__name__.lower()}.rest_{view.action}"
        ):
            return True
        return False
