import factory

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from core.shortcuts import convert_to_furigana, convert_to_ascii

from faker import Factory


fake = Factory.create('ja_JP')


class UserFactory(factory.django.DjangoModelFactory):
    """
        User Factory
    """

    class Meta:
        model = get_user_model()

    first_name = factory.LazyAttribute(lambda o: fake.first_name())
    last_name = factory.Sequence(
        lambda n: f'{fake.last_name()}{n}'
    )
    email = factory.LazyAttribute(
        lambda o: (f'{convert_to_ascii(o.first_name)}_{convert_to_ascii(o.last_name)}'
                   f'@{fake.free_email_domain()}'.lower())
    )

    furigana_fname = factory.LazyAttribute(
        lambda o: convert_to_furigana(o.first_name)
    )
    furigana_lname = factory.LazyAttribute(
        lambda o: convert_to_furigana(o.last_name)
    )
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
