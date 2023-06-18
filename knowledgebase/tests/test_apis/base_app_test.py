from core.tests.base_test import BaseWebTestCases
from faker import Faker

from knowledgebase.tests.factories.knowledgebase import KnowledgeBaseFactory
from users.tests.factories.user import UserFactory


class KnowledgeBaseTestCases(BaseWebTestCases):

    model_manager = None
    grouped_model_manager = None

    fake = Faker()

    app_name = "knowledgebase"
    unique_string = "YD122E"

    def setUp(self, *args, **kwargs):
        KnowledgeBaseFactory(description=self.unique_string, is_public=False)
        KnowledgeBaseFactory(title=self.unique_string, is_public=True)
        KnowledgeBaseFactory(is_public=True)
        KnowledgeBaseFactory(description=self.unique_string, is_public=True)
        a = KnowledgeBaseFactory(is_public=True)
        b = KnowledgeBaseFactory(is_public=True)
        b_owner = UserFactory(first_name=self.unique_string)
        a_owner = UserFactory(last_name=self.unique_string)
        b.owner = b_owner
        b.save()
        a.owner = a_owner
        a.save()

        super().setUp(args, kwargs)
