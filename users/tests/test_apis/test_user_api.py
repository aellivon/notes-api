import pytz

from django.urls import reverse
from datetime import datetime

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
            'date_joined': self.fake.iso8601(tzinfo=pytz.timezone('Asia/Tokyo')),
            'avatar_url': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII="
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
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('first_name'), self.data_update.get('first_name'))
        self.assertEqual(response.json().get('last_name'), self.data_update.get('last_name'))
        self.assertEqual(response.json().get('email'), self.data_update.get('email'))
        self.assertEqual(response.json().get('furigana_fname'), self.data_update.get('furigana_fname'))
        self.assertEqual(response.json().get('furigana_lname'), self.data_update.get('furigana_lname'))
        self.assertEqual(response.json().get('position'), self.data_update.get('position'))
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
        self.assertEqual(
            datetime.fromisoformat(response.json().get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo')),
            datetime.fromisoformat(self.data_update.get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo'))
        )

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
        self.assertEqual(
            datetime.fromisoformat(response.json().get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo')),
            datetime.fromisoformat(self.data_update.get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo'))
        )

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
        self.assertEqual(
            datetime.fromisoformat(response.json().get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo')),
            datetime.fromisoformat(self.data_update.get('date_joined')).astimezone(pytz.timezone('Asia/Tokyo'))
        )


class UserCreateTestCases(UserTestCases):
    """
        Tests concerning creating a user
    """

    base_name = "user"

    data_update = None

    def test_create_user_with_proper_permissions_succeeds(self):
        pass

    def test_create_user_with_supueruser_permission_succeeds(self):
        pass

    def test_crete_user_with_unauthorize_fails(self):
        pass
