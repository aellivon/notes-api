# Creating the base for our all tests across the app
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework.test import APIClient, APITestCase

from users.tests.factories.user import UserFactory


class BaseWebTestCases(APITestCase):
    """
        The base for all our testcases, currently houses the user creation
    """

    default_password = "password"

    active_user = None
    super_user = None
    other_user = None
    staff_user = None

    access_token = ""

    fake = Faker()

    user_model = get_user_model()

    # Simulating a request
    client = APIClient()

    def setUp(self, *args, **kwargs):
        """
            Creating an active user
            Note, we are using the funciton 'create user' so that the password will be hashed
        """
        self.super_user = UserFactory(is_admin=True)
        self.staff_user = UserFactory(is_staff=True)
        self.active_user = UserFactory()
        self.inactive_user = UserFactory(is_active=False)
        self.other_user = UserFactory()

    def login(self, user, login_scheme="", password=None):

        email = user.email

        if not password:
            password = self.default_password

        if login_scheme == "JWT":
            res = self.client.post(reverse('users:rest_login'), {"email": email, "password": password})
            self.access_token = res.data.get("access_token", "")
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        else:
            # Use default session
            self.client.login(email=email, password=self.default_password)

    def login_active_user(self, login_scheme=""):
        """
            Logins an active user to our client
        """
        self.login(self.active_user, login_scheme)

    def login_inactive_user(self, login_scheme=""):
        """
            Logins an inactive user to our client
        """
        self.login(self.inactive_user, login_scheme)

    def login_other_user(self, login_scheme=""):
        """
            Logins as other user to test permissions
        """
        self.login(self.other_user, login_scheme)

    def login_super_user(self, login_scheme=""):
        """
            Logins super user
        """
        self.login(self.super_user, login_scheme)

    def login_staff_user(self, login_scheme=""):
        """
            Logins staff user
        """
        self.login(self.staff_user, login_scheme)

    def _get_app_and_base_name(self):
        """
            Gets the root url of a viewset
        """
        if self.app_name:
            return f"{self.app_name}:{self.base_name}"
        return self.base_name

    def get_list_url(self):
        """
            Gets the app name with the view name and append it with list
        """
        return f"{self._get_app_and_base_name()}-list"

    def get_detail_url(self):
        """
            Gets the app name with the view name and append it with detail
        """
        return f"{self._get_app_and_base_name()}-detail"

    def get_root_url(self):
        return f"{self._get_app_and_base_name()}"
