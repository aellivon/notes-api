from core.tests.base_test import BaseWebTestCases
from faker import Faker
from django.contrib.auth.models import Permission
from users.tests.factories.user import UserFactory
from users.tests.factories.group import GroupFactory


class UserTestCases(BaseWebTestCases):
    """
       Base test for users
    """

    fake = Faker()

    user_manager = None
    app_name = "users"

    group_a = None
    unique_string = "YD122E"
    grouped_user_manager = None

    def login_user_manager(self, login_scheme="JWT"):
        """
            Logins an active user to our client
        """
        self.login(self.user_manager, login_scheme)

    def login_group_user_manager(self, login_scheme="JWT"):
        """
            Logins an active user to our client
        """
        self.login(self.grouped_user_manager, login_scheme)

    def setUp(self, *args, **kwargs):
        """
            Creating user that is concern on user managing
        """
        self.user_manager = UserFactory()
        view_perm = Permission.objects.get(codename="view_user")
        update_user_perm = Permission.objects.get(codename="change_user")
        create_user_perm = Permission.objects.get(codename="add_user")
        delete_user_perm = Permission.objects.get(codename="delete_user")
        group_view_perm = Permission.objects.get(codename="view_group")

        self.user_manager.user_permissions.add(view_perm)
        self.user_manager.user_permissions.add(update_user_perm)
        self.user_manager.user_permissions.add(create_user_perm)
        self.user_manager.user_permissions.add(group_view_perm)
        self.user_manager.user_permissions.add(delete_user_perm)
        self.user_manager.save()

        UserFactory(first_name=self.unique_string)
        UserFactory(last_name=self.unique_string)
        UserFactory(email=f"{self.unique_string}@aellivon.com")
        UserFactory(furigana_fname=self.unique_string)
        self.grouped_user_manager = UserFactory(furigana_lname=self.unique_string)
        user_group_a = UserFactory(position=self.unique_string)

        self.group_a = GroupFactory()
        self.group_a.user_set.add(user_group_a)

        group_b = GroupFactory()
        group_b.user_set.add(self.grouped_user_manager)
        group_b.permissions.add(view_perm)
        group_b.permissions.add(group_view_perm)
        group_b.permissions.add(update_user_perm)
        group_b.permissions.add(create_user_perm)
        group_b.permissions.add(delete_user_perm)

        super().setUp(args, kwargs)
