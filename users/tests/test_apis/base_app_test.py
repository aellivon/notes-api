from core.tests.base_test import BaseWebTestCases
from django.contrib.auth.models import Permission
from users.tests.factories.user import UserFactory


class UserTestCases(BaseWebTestCases):
    """
       Base test for users
    """

    user_manager = None
    app_name = "users"

    def login_user_manager(self, login_scheme="JWT"):
        """
            Logins an active user to our client
        """
        self.login(self.user_manager.email, login_scheme)

    def setUp(self, *args, **kwargs):
        """
            Creating user that is concern on user managing
        """
        self.user_manager = UserFactory()
        perm = Permission.objects.get(codename="view_user")
        self.user_manager.user_permissions.add(perm)
        self.user_manager.save()
        super().setUp(args, kwargs)
