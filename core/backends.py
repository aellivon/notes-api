from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission

from django.contrib.auth import get_user_model


class ModelBackend(ModelBackend):

    def _get_user_rest_permissions(self, user_obj):
        return user_obj.user_permissions.all()

    def _get_group_rest_permissions(self, user_obj):
        user_groups_field = get_user_model()._meta.get_field('groups')
        user_groups_query = 'group__%s' % user_groups_field.related_query_name()
        return Permission.objects.filter(**{user_groups_query: user_obj})

    def _get_rest_permissions(self, user_obj, obj, from_name):
        """
        Return the permissions of `user_obj` from `from_name`. `from_name` can
        be either "group" or "user" to return permissions from
        `_get_group_rest_permissions` or `_get_user_rest_permissions` respectively.
        """
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()

        perm_cache_name = '_%s_rest_perm_cache' % from_name
        if not hasattr(user_obj, perm_cache_name):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = getattr(self, '_get_%s_rest_permissions' % from_name)(user_obj)

            dotted_list_permission = []

            for perm in perms:
                key = list(perm.content_type.natural_key())
                key.append(perm.codename)
                dotted_permission = ".".join(key)
                dotted_list_permission.append(dotted_permission)

            setattr(user_obj, perm_cache_name, dotted_list_permission)
        return getattr(user_obj, perm_cache_name)

    def get_user_rest_permissions(self, user_obj, obj=None):
        """
        Return a set of permission strings the user `user_obj` has from their
        `user_permissions`.
        """
        return self._get_rest_permissions(user_obj, obj, 'user')

    def get_group_rest_permissions(self, user_obj, obj=None):
        """
        Return a set of permission strings the user `user_obj` has from the
        groups they belong.
        """
        return self._get_rest_permissions(user_obj, obj, 'group')

    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = {
                *self.get_user_rest_permissions(user_obj, obj=obj),
                *self.get_group_rest_permissions(user_obj, obj=obj),
                *self.get_user_permissions(user_obj, obj=obj),
                *self.get_group_permissions(user_obj, obj=obj),
            }
        print(user_obj._perm_cache)
        return user_obj._perm_cache
