from django.urls import reverse

from rest_framework import status

from .base_app_test import UserTestCases


class UserListTestCases(UserTestCases):
    """
        Test cases concerning record list
    """

    base_name = "user"

    def test_get_users_list_has_permission_succeeds(self):
        self.login_user_manager()
        response = self.client.get(reverse(self.get_list_url()))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users_list_without_permission_fails(self):
        self.login_active_user()
        response = self.client.get(reverse(self.get_list_url()))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_users_list_unauthorized_fails(self):
        response = self.client.get(reverse(self.get_list_url()))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_list_is_superuser_succeeds(self):
        self.login_super_user("JWT")
        response = self.client.get(reverse(self.get_list_url()))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_list_with_group_permission_succeeds(self):
        self.login_group_user_manager()
        response = self.client.get(reverse(self.get_list_url()))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_list_with_permission_and_search_filter_succeeds(self):
        self.login_user_manager()
        response = self.client.get(
            reverse(self.get_list_url()),
            data={"search": self.unique_string}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count", 0), 6)

    def test_get_user_with_permission_and_user_group_filter_succeeds(self):
        self.login_user_manager()
        response = self.client.get(
            reverse(self.get_list_url()),
            data={"group": self.group_a.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count", 0), 1)

    def test_get_user_with_permission_and_user_status_filter_succeeds(self):
        self.login_user_manager()
        response = self.client.get(
            reverse(self.get_list_url()),
            data={"status": "archived"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count", 0), 1)

    def test_get_user_with_permission_and_admin_status_filter_succeeds(self):
        self.login_user_manager()
        response = self.client.get(
            reverse(self.get_list_url()),
            data={"type": "admin"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count", 0), 1)
