import random

import factory

from thoughts.models import Thought, Tag, User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Faker('username')


class TagFactory(factory.Factory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: f'tag_{n}')


class ThoughtFactory(factory.Factory):
    class Meta:
        model = Thought

    text = factory.Faker('sentence')
    author = factory.SubFactory(UserFactory)
    is_editable = random.choice([True, False])

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
