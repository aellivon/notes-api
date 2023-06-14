import json

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.db import transaction

from core.shortcuts import get_object_or_None


class Command(BaseCommand):
    help = 'Adds or Updates the group that was specified on the permissions/base.py'

    def handle(self, *args, **options):
        coupled_permission = None
        user_type_permissions = None

        coupled_permission = open("core/permissions/presets/coupled_permission.json")
        user_type_permissions = open("core/permissions/presets/user_type_permissions.json")

        user_types = json.load(user_type_permissions)
        permission_bundle = json.load(coupled_permission)

        with transaction.atomic():
            for user_type_key in user_types:
                permission_list = user_types[user_type_key]
                for perm in permission_list:
                    to_add_perms = permission_bundle.get(perm, [perm])
                    group, _ = Group.objects.get_or_create(
                        code_reference=user_type_key
                    )
                    group.name = user_type_key
                    for to_add_perm in to_add_perms:
                        condition_array = list(to_add_perm.split("."))
                        model = condition_array[0]
                        code_name = condition_array[1]
                        permission_instance = get_object_or_None(
                            Permission,
                            content_type__model=model,
                            codename=code_name
                        )

                        if not permission_instance:
                            raise Exception(f"Permission {to_add_perm} does not exists!")

                        group.permissions.add(permission_instance)
                        group.save()
