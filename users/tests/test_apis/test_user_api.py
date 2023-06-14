import pytz

from django.urls import reverse
from datetime import datetime

from rest_framework import status
from core.shortcuts import convert_to_furigana, convert_to_ascii
from users.tests.factories.user import UserFactory

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
            'date_joined': self.fake.iso8601(tzinfo=pytz.timezone('Asia/Tokyo')),
            'avatar_url': ("data:image/png;base64, "
                           "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4"
                           "//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")
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

    def test_update_user_with_no_match_id_fails(self):
        self.login_other_user()
        response = self.client.patch(
            reverse(self.get_detail_url(), kwargs={"pk": 999999}),
            data=self.data_update
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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
        self.assertIn(".png", response.json().get("avatar_url"))
        self.assertNotEqual(
            datetime.fromisoformat(response.json().get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo')),
            datetime.fromisoformat(self.data_update.get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo'))
        )

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
        self.assertIn(".png", response.json().get("avatar_url"))
        self.assertEqual(
            datetime.fromisoformat(response.json().get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo')),
            datetime.fromisoformat(self.data_update.get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo'))
        )

    def test_update_user_with_group_can_update_user_permission_succeeds(self):
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
        self.assertIn(".png", response.json().get("avatar_url"))
        self.assertEqual(
            datetime.fromisoformat(response.json().get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo')),
            datetime.fromisoformat(self.data_update.get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo'))
        )

    def test_update_user_with_admin_succeeds(self):
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
        self.assertIn(".png", response.json().get("avatar_url"))
        self.assertEqual(
            datetime.fromisoformat(response.json().get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo')),
            datetime.fromisoformat(self.data_update.get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo'))
        )


class UserCreateTestCases(UserTestCases):
    """
        Tests concerning creating a user
    """

    base_name = "user"

    data_create = None

    def __init__(self, *args, **kwargs):
        self.data_create = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'email': (f'{convert_to_ascii(self.fake.first_name())}_{convert_to_ascii(self.fake.last_name())}'
                      f'@{self.fake.free_email_domain()}'.lower()),
            'furigana_fname': convert_to_furigana(self.fake.first_name()),
            'furigana_lname': convert_to_furigana(self.fake.first_name()),
            'position': self.fake.company(),
            'date_joined': self.fake.iso8601(tzinfo=pytz.timezone('Asia/Tokyo')),
            'avatar_url': ("data:image/png;base64, "
                           "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4"
                           "//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")
        }
        super().__init__(*args, **kwargs)

    def test_create_user_with_unauthorized_fails(self):
        response = self.client.post(
            reverse(self.get_list_url()),
            data=self.data_create
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_non_admin_fails(self):
        self.login_active_user()
        response = self.client.post(
            reverse(self.get_list_url()),
            data=self.data_create
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_with_can_create_user_permission_succeeds(self):
        self.login_user_manager()
        response = self.client.post(
            reverse(self.get_list_url()),
            data=self.data_create
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('first_name'), self.data_create.get('first_name'))
        self.assertEqual(response.json().get('last_name'), self.data_create.get('last_name'))
        self.assertEqual(response.json().get('email'), self.data_create.get('email'))
        self.assertEqual(response.json().get('furigana_fname'), self.data_create.get('furigana_fname'))
        self.assertEqual(response.json().get('furigana_lname'), self.data_create.get('furigana_lname'))
        self.assertEqual(response.json().get('position'), self.data_create.get('position'))
        self.assertEqual(
            datetime.fromisoformat(response.json().get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo')),
            datetime.fromisoformat(self.data_create.get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo'))
        )
        self.assertIn(".png", response.json().get("avatar_url"))

    def test_create_user_with_group_can_create_user_permission_succeeds(self):
        self.login_group_user_manager()
        response = self.client.post(
            reverse(self.get_list_url()),
            data=self.data_create
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('first_name'), self.data_create.get('first_name'))
        self.assertEqual(response.json().get('last_name'), self.data_create.get('last_name'))
        self.assertEqual(response.json().get('email'), self.data_create.get('email'))
        self.assertEqual(response.json().get('furigana_fname'), self.data_create.get('furigana_fname'))
        self.assertEqual(response.json().get('furigana_lname'), self.data_create.get('furigana_lname'))
        self.assertEqual(response.json().get('position'), self.data_create.get('position'))
        self.assertEqual(
            datetime.fromisoformat(response.json().get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo')),
            datetime.fromisoformat(self.data_create.get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo'))
        )
        self.assertIn(".png", response.json().get("avatar_url"))

    def test_create_user_with_admin_succeeds(self):
        self.login_super_user("JWT")
        response = self.client.post(
            reverse(self.get_list_url()),
            data=self.data_create
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('first_name'), self.data_create.get('first_name'))
        self.assertEqual(response.json().get('last_name'), self.data_create.get('last_name'))
        self.assertEqual(response.json().get('email'), self.data_create.get('email'))
        self.assertEqual(response.json().get('furigana_fname'), self.data_create.get('furigana_fname'))
        self.assertEqual(response.json().get('furigana_lname'), self.data_create.get('furigana_lname'))
        self.assertEqual(response.json().get('position'), self.data_create.get('position'))
        self.assertEqual(
            datetime.fromisoformat(response.json().get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo')),
            datetime.fromisoformat(self.data_create.get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo'))
        )
        self.assertIn(".png", response.json().get("avatar_url"))


class UserRetrieveTestCases(UserTestCases):

    base_name = "user"

    def test_get_user_detail_has_permission_succeeds(self):
        self.login_user_manager()
        response = self.client.get(reverse(self.get_detail_url(), kwargs={"pk": self.active_user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detail_without_permission_fails(self):
        self.login_active_user()
        response = self.client.get(reverse(self.get_detail_url(), kwargs={"pk": self.active_user.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_detail_unauthorized_fails(self):
        response = self.client.get(reverse(self.get_detail_url(), kwargs={"pk": self.active_user.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_detail_is_superuser_succeeds(self):
        self.login_super_user("JWT")
        response = self.client.get(reverse(self.get_detail_url(), kwargs={"pk": self.active_user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detail_with_group_permission_succeeds(self):
        self.login_group_user_manager()
        response = self.client.get(reverse(self.get_detail_url(), kwargs={"pk": self.active_user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detail_with_no_corresponding_id_fails(self):
        self.login_group_user_manager()
        response = self.client.get(reverse(self.get_detail_url(), kwargs={"pk": 999999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserArchiveViewSet(UserTestCases):

    base_name = "user"

    def test_archive_user_has_permission_succeeds(self):
        self.login_user_manager()
        to_delete_user = UserFactory()
        response = self.client.delete(reverse(self.get_detail_url(), kwargs={"pk": to_delete_user.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_archive_user_without_permission_fails(self):
        self.login_active_user()
        to_delete_user = UserFactory()
        response = self.client.delete(reverse(self.get_detail_url(), kwargs={"pk": to_delete_user.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_archive_user_unauthorized_fails(self):
        to_delete_user = UserFactory()
        response = self.client.delete(reverse(self.get_detail_url(), kwargs={"pk": to_delete_user.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_archive_user_is_superuser_succeeds(self):
        self.login_super_user("JWT")
        to_delete_user = UserFactory()
        response = self.client.delete(reverse(self.get_detail_url(), kwargs={"pk": to_delete_user.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_archive_user_with_group_permission_succeeds(self):
        self.login_group_user_manager()
        to_delete_user = UserFactory()
        response = self.client.delete(reverse(self.get_detail_url(), kwargs={"pk": to_delete_user.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_archive_user_detail_with_no_corresponding_id_fails(self):
        self.login_group_user_manager()
        response = self.client.delete(reverse(self.get_detail_url(), kwargs={"pk": 999999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_archive_user_with_owner_fails(self):
        # Prevents the user from shooting themselves on the foot
        self.login_active_user()
        response = self.client.delete(
            reverse(self.get_detail_url(), kwargs={"pk": self.active_user.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
