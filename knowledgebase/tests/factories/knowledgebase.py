import factory

from knowledgebase.models import KnowledgeBase

from faker import Factory

from users.tests.factories.user import UserFactory


fake = Factory.create('ja_JP')


class KnowledgeBaseFactory(factory.django.DjangoModelFactory):
    """
        User Factory
    """

    class Meta:
        model = KnowledgeBase

    title = factory.LazyAttribute(lambda o: fake.sentence())
    description = factory.LazyAttribute(lambda o: fake.paragraph())
    owner = factory.SubFactory(UserFactory)
    is_public = factory.LazyAttribute(lambda o: fake.boolean())
