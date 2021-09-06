import random

import factory

from thoughts.models import Thought, Tag, User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: f'tag_{n}')


class ThoughtFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Thought

    author = factory.SubFactory(UserFactory)
    text = factory.Faker('sentence')
    is_editable = random.choice([True, False])

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
