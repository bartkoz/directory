import string

import factory
from django.contrib.auth.models import User
from factory.fuzzy import FuzzyInteger, FuzzyText

from app.models import Teacher, Subject


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = "test"


class SubjectFactory(factory.Factory):
    class Meta:
        model = Subject

    name = FuzzyText(length=12, chars=string.ascii_letters)


class TeacherFactory(factory.Factory):
    class Meta:
        model = Teacher

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email_address = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    room_number = str(FuzzyInteger(low=0, high=10))
    subjects_taught = factory.RelatedFactory(SubjectFactory, "name")
