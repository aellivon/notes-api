from django.urls import reverse
from rest_framework import status

from knowledgebase.tests.factories.knowledgebase import KnowledgeBaseFactory
from users.tests.factories.user import UserFactory

from .base_app_test import KnowledgeBaseTestCases


class KnowledgeBaseCreateTestCases(KnowledgeBaseTestCases):

    def __init__(self, *args, **kwargs):
        self.data_create = {
            'title': self.fake.sentence(),
            'description': self.fake.paragraph(),
            'is_public': self.fake.boolean()
        }
        self.malicous_data_create = {
            'title': self.fake.sentence(),
            'description': self.fake.paragraph(),
            'is_public': self.fake.boolean(),
            'owner': UserFactory().pk,
            'id': 999
        }
        super().__init__(*args, **kwargs)

    base_name = "knowledgebase"

    def test_create_with_authroziation_succeeds(self):
        self.login_active_user(login_scheme="JWT")
        response = self.client.post(
            reverse(self.get_list_url()),
            data=self.data_create
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('title'), self.data_create.get('title'))
        self.assertEqual(response.json().get('description'), self.data_create.get('description'))
        self.assertEqual(response.json().get('is_public'), self.data_create.get('is_public'))

    def test_create_with_unauthorized_fails(self):
        response = self.client.post(
            reverse(self.get_list_url()),
            data=self.data_create
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_with_authorization_but_malicious_data_ignored_but_success(self):
        self.login_active_user(login_scheme="JWT")
        response = self.client.post(
            reverse(self.get_list_url()),
            data=self.malicous_data_create
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('title'), self.malicous_data_create.get('title'))
        self.assertEqual(response.json().get('description'), self.malicous_data_create.get('description'))
        self.assertEqual(response.json().get('is_public'), self.malicous_data_create.get('is_public'))
        self.assertNotEqual(response.json().get('id'), self.malicous_data_create.get('id'))
        self.assertNotEqual(response.json().get('owner'), self.malicous_data_create.get('owner'))


class KnowledgebaseMyListTestCases(KnowledgeBaseTestCases):

    base_name = "knowledgebase"
    action = "all"

    def test_get_kb_list_unauthorized_fails(self):
        response = self.client.get(reverse(self.get_list_url()))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_kb_list_with_authoization_can_get_public_notes(self):
        self.login_active_user(login_scheme="JWT")
        KnowledgeBaseFactory(owner=self.active_user, is_public=True)
        KnowledgeBaseFactory(owner=self.active_user, is_public=False)
        response = self.client.get(reverse(self.get_list_url()))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count", 0), 2)

    def test_get_kb_list_with_search_text_can_filter_properly(self):

        self.login_active_user(login_scheme="JWT")

        KnowledgeBaseFactory(owner=self.active_user, description=self.unique_string)
        KnowledgeBaseFactory(owner=self.active_user, title=self.unique_string)
        KnowledgeBaseFactory(owner=self.active_user, description=self.unique_string)

        response = self.client.get(
            reverse(self.get_list_url()),
            data={"search": self.unique_string}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count", 0), 3)


class KnowledgebaseListAllTestCases(KnowledgeBaseTestCases):

    base_name = "knowledgebase"
    action = "all"

    def test_get_kb_list_unauthorized_fails(self):
        response = self.client.get(reverse(self.get_action_url(self.action)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_kb_list_with_authoization_can_get_public_notes(self):
        self.login_active_user(login_scheme="JWT")
        response = self.client.get(reverse(self.get_action_url(self.action)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count", 0), 5)

    def test_get_kb_list_with_search_text_can_filter_properly(self):
        self.login_active_user(login_scheme="JWT")
        response = self.client.get(
            reverse(self.get_action_url(self.action)),
            data={"search": self.unique_string}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count", 0), 4)


class KnowledgebaseRetrieveTestCases(KnowledgeBaseTestCases):

    base_name = "knowledgebase"

    def test_get_kb_retrieve_unauthorized_fails(self):
        response = self.client.get(reverse(self.get_list_url()))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_kb_retrieve_with_authoization_can_get_public_notes_success(self):
        self.login_active_user(login_scheme="JWT")
        knowledge_base_factory = KnowledgeBaseFactory(owner=self.other_user, is_public=True)
        response = self.client.get(
            reverse(self.get_detail_url(), kwargs={"pk": knowledge_base_factory.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_kb_retrieve_with_auhtorization_cannot_get_private_notes_of_others_fails(self):
        self.login_active_user(login_scheme="JWT")
        knowledge_base_factory = KnowledgeBaseFactory(owner=self.other_user, is_public=False)
        response = self.client.get(
            reverse(self.get_detail_url(), kwargs={"pk": knowledge_base_factory.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_kb_retrieve_with_autorization_can_get_owned_private_notes_success(self):
        self.login_active_user(login_scheme="JWT")
        knowledge_base_factory = KnowledgeBaseFactory(owner=self.active_user, is_public=False)
        response = self.client.get(
            reverse(self.get_detail_url(), kwargs={"pk": knowledge_base_factory.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_kb_retrieve_with_autorization_can_get_owned_public_notes_success(self):
        self.login_active_user(login_scheme="JWT")
        knowledge_base_factory = KnowledgeBaseFactory(owner=self.active_user, is_public=True)
        response = self.client.get(
            reverse(self.get_detail_url(), kwargs={"pk": knowledge_base_factory.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_kb_retrieve_with_id_not_found_fails(self):
        self.login_active_user(login_scheme="JWT")
        KnowledgeBaseFactory(owner=self.active_user, is_public=True)
        response = self.client.get(
            reverse(self.get_detail_url(), kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class KnowledgeBaseUpdateTestCases(KnowledgeBaseFactory):

    def __init__(self, *args, **kwargs):
        self.data_update = {
            'title': self.fake.sentence(),
            'description': self.fake.paragraph(),
            'is_public': self.fake.boolean()
        }
        self.malicous_data_update = {
            'title': self.fake.sentence(),
            'description': self.fake.paragraph(),
            'is_public': self.fake.boolean(),
            'owner': UserFactory().pk,
            'id': 999
        }
        super().__init__(*args, **kwargs)

    base_name = "knowledgebase"

    def test_patch_kb_update_unauthorized_fails(self):
        knowledge_base_factory = KnowledgeBaseFactory(owner=self.active_user)
        response = self.client.patch(reverse(self.get_detail_url(), kwargs={"pk": knowledge_base_factory.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_kb_update_authorized_and_owner_succeeds(self):
        self.login_active_user(login_scheme="JWT")
        knowledge_base_factory = KnowledgeBaseFactory(owner=self.active_user)
        response = self.client.patch(
            reverse(self.get_detail_url(), kwargs={"pk": knowledge_base_factory.id}),
            data=self.data_update
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), self.data_update.get('title'))
        self.assertEqual(response.json().get('description'), self.data_update.get('description'))
        self.assertEqual(response.json().get('is_public'), self.data_update.get('is_public'))

    def test_patch_kb_update_auhtorized_but_other_kb_update_fails(self):
        self.login_other_user(login_scheme="JWT")
        knowledge_base_factory = KnowledgeBaseFactory(owner=self.active_user)
        response = self.client.patch(
            reverse(self.get_detail_url(), kwargs={"pk": knowledge_base_factory.id}),
            data=self.data_update
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_kb_update_authorized_and_owner_cannot_update_owner_and_id(self):
        self.login_active_user(login_scheme="JWT")
        knowledge_base_factory = KnowledgeBaseFactory(owner=self.active_user)
        response = self.client.patch(
            reverse(self.get_detail_url(), kwargs={"pk": knowledge_base_factory.id}),
            data=self.malicous_data_update
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), self.malicous_data_update.get('title'))
        self.assertEqual(response.json().get('description'), self.malicous_data_update.get('description'))
        self.assertEqual(response.json().get('is_public'), self.malicous_data_update.get('is_public'))
        self.assertNotEqual(response.json().get('id'), self.malicous_data_update.get('id'))
        self.assertNotEqual(response.json().get('owner'), self.malicous_data_update.get('owner'))

    def test_put_kb_update_authorized_and_owner_fails(self):
        self.login_active_user(login_scheme="JWT")
        knowledge_base_factory = KnowledgeBaseFactory(owner=self.active_user)
        response = self.client.put(
            reverse(self.get_detail_url(), kwargs={"pk": knowledge_base_factory.id}),
            data=self.data_update
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_kb_but_no_corresponding_id_not_found(self):
        self.login_active_user(login_scheme="JWT")
        response = self.client.patch(
            reverse(self.get_detail_url(), kwargs={"pk": 999999}),
            data=self.data_update
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class KnowledgeBaseArchiveTestCases(KnowledgeBaseTestCases):

    base_name = "knowledgebase"

    def test_archive_owned_kb_suceeds(self):
        self.login_active_user(login_scheme="JWT")
        knowledge_base_factory = KnowledgeBaseFactory(owner=self.active_user, is_public=True)
        response = self.client.delete(
            reverse(self.get_detail_url(), kwargs={"pk": knowledge_base_factory.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_archive_owned_private_kb_suceeds(self):
        self.login_active_user(login_scheme="JWT")
        knowledge_base_factory = KnowledgeBaseFactory(owner=self.active_user, is_public=False)
        response = self.client.delete(
            reverse(self.get_detail_url(), kwargs={"pk": knowledge_base_factory.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_archive_other_kb_fails(self):
        self.login_active_user(login_scheme="JWT")
        knowledge_base_factory = KnowledgeBaseFactory(owner=self.other_user, is_public=True)
        response = self.client.delete(
            reverse(self.get_detail_url(), kwargs={"pk": knowledge_base_factory.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_archive_private_and_other_kb_fails(self):
        self.login_active_user(login_scheme="JWT")
        knowledge_base_factory = KnowledgeBaseFactory(owner=self.other_user, is_public=False)
        response = self.client.delete(
            reverse(self.get_detail_url(), kwargs={"pk": knowledge_base_factory.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_archive_unauth_kb_fails(self):
        knowledge_base_factory = KnowledgeBaseFactory(owner=self.other_user)
        response = self.client.delete(
            reverse(self.get_detail_url(), kwargs={"pk": knowledge_base_factory.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_archive_no_corresponding_fails(self):
        self.login_active_user(login_scheme="JWT")
        response = self.client.delete(
            reverse(self.get_detail_url(), kwargs={"pk": 9999})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
