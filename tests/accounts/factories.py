import factory

from accounts.models import User
from faker import Faker
fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


    email = "test@test.com"
    first_name = "first_name"
    last_name = "last_name"
    