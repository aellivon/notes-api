import factory

from django.contrib.auth.models import Group

from faker import Factory


fake = Factory.create('ja_JP')


class GroupFactory(factory.django.DjangoModelFactory):
    """
        User Factory
    """

    class Meta:
        model = Group

    name = factory.LazyAttribute(lambda o: fake.company())
