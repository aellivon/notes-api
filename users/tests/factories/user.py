import factory

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """
        User Factory
    """

    class Meta:
        model = get_user_model()

    email = factory.Sequence(
        lambda o: f'{fake.first_name()}{fake.last_name()}{o}@{fake.free_email_domain()}'.lower()
    )

    first_name = factory.LazyAttribute(lambda o: fake.first_name())
    last_name = factory.LazyAttribute(lambda o: fake.last_name())

    furigana_fname = factory.LazyAttribute(lambda o: fake.first_name())
    furigana_lname = factory.LazyAttribute(lambda o: fake.last_name())
    position = factory.LazyAttribute(lambda o: fake.word())
    avatar_url = factory.django.ImageField(color='blue')

    password = make_password('password')

    is_superuser = False
    is_staff = False
    is_active = True

    class Params:
        # declare a trait that adds relevant parameters for admin users
        is_admin = factory.Trait(
            is_superuser=True,
            is_staff=True
        )
