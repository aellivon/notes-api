from django.urls import reverse

from rest_framework import status
from core.shortcuts import convert_to_furigana, convert_to_ascii

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


class UserUpdateTestCases(UserTestCases):
    """
        Tests concerning updating a user
    """

    base_name = "user"

    data_update = None

    def __init__(self, *args, **kwargs):
        self.data_update = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'email': (f'{convert_to_ascii(self.fake.first_name())}_{convert_to_ascii(self.fake.last_name())}'
                      f'@{self.fake.free_email_domain()}'.lower()),
            'furigana_fname': convert_to_furigana(self.fake.first_name()),
            'furigana_lname': convert_to_furigana(self.fake.first_name()),
            'position': self.fake.company(),
        }
        super().__init__(*args, **kwargs)

    def test_update_user_with_unauthorize_fails(self):
        response = self.client.patch(
            reverse(self.get_detail_url(), kwargs={"pk": self.active_user.id}),
            data=self.data_update
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_with_non_owner_and_non_admin_fails(self):
        self.login_other_user()
        response = self.client.patch(
            reverse(self.get_detail_url(), kwargs={"pk": self.active_user.id}),
            data=self.data_update
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_with_owner_succeeds(self):
        self.login_active_user("JWT")
        response = self.client.patch(
            reverse(self.get_detail_url(), kwargs={"pk": self.active_user.id}),
            data=self.data_update
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('first_name'), self.data_update.get('first_name'))
        self.assertEqual(response.json().get('last_name'), self.data_update.get('last_name'))
        self.assertEqual(response.json().get('email'), self.data_update.get('email'))
        self.assertEqual(response.json().get('furigana_fname'), self.data_update.get('furigana_fname'))
        self.assertEqual(response.json().get('furigana_lname'), self.data_update.get('furigana_lname'))
        self.assertEqual(response.json().get('position'), self.data_update.get('position'))

    def test_put_even_with_superuser_fails(self):
        self.login_super_user("JWT")
        response = self.client.put(
            reverse(self.get_detail_url(), kwargs={"pk": self.active_user.id}),
            data=self.data_update
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_with_can_update_user_permission_succeeds(self):
        self.login_user_manager()
        response = self.client.patch(
            reverse(self.get_detail_url(), kwargs={"pk": self.active_user.id}),
            data=self.data_update
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('first_name'), self.data_update.get('first_name'))
        self.assertEqual(response.json().get('last_name'), self.data_update.get('last_name'))
        self.assertEqual(response.json().get('email'), self.data_update.get('email'))
        self.assertEqual(response.json().get('furigana_fname'), self.data_update.get('furigana_fname'))
        self.assertEqual(response.json().get('furigana_lname'), self.data_update.get('furigana_lname'))
        self.assertEqual(response.json().get('position'), self.data_update.get('position'))

    def test_update_listing_with_group_can_update_user_permission_succeeds(self):
        self.login_group_user_manager()
        response = self.client.patch(
            reverse(self.get_detail_url(), kwargs={"pk": self.active_user.id}),
            data=self.data_update
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('first_name'), self.data_update.get('first_name'))
        self.assertEqual(response.json().get('last_name'), self.data_update.get('last_name'))
        self.assertEqual(response.json().get('email'), self.data_update.get('email'))
        self.assertEqual(response.json().get('furigana_fname'), self.data_update.get('furigana_fname'))
        self.assertEqual(response.json().get('furigana_lname'), self.data_update.get('furigana_lname'))
        self.assertEqual(response.json().get('position'), self.data_update.get('position'))

    def test_update_listing_with_admin_succeeds(self):
        self.login_super_user("JWT")
        response = self.client.patch(
            reverse(self.get_detail_url(), kwargs={"pk": self.active_user.id}),
            data=self.data_update
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('first_name'), self.data_update.get('first_name'))
        self.assertEqual(response.json().get('last_name'), self.data_update.get('last_name'))
        self.assertEqual(response.json().get('email'), self.data_update.get('email'))
        self.assertEqual(response.json().get('furigana_fname'), self.data_update.get('furigana_fname'))
        self.assertEqual(response.json().get('furigana_lname'), self.data_update.get('furigana_lname'))
        self.assertEqual(response.json().get('position'), self.data_update.get('position'))
