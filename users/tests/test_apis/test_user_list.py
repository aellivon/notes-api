from django.urls import reverse

from rest_framework import status

from .base_app_test import UserTestCases


class UserListTestCases(UserTestCases):
    """
        Test cases concerning record list
    """

    base_name = "user"

    def test_get_users_list_has_permission_succeeds(self):
        self.login_active_user()
        response = self.client.get(reverse(self.get_list_url()))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users_list_unauthorized_fails(self):
        response = self.client.get(reverse(self.get_list_url()))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
