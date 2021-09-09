import random

import pytest
from faker import Faker
from pytest_factoryboy import register
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

from .factories import TagFactory, ThoughtFactory, UserFactory

fake = Faker()

register(ThoughtFactory)  # = thought_factory fixture
register(TagFactory)  # = tag_factory
register(UserFactory)  # = user_factory


@pytest.fixture
def user(db, user_factory):
    return user_factory()


@pytest.fixture
def custom_user(db, user_factory):
    """Add the ability to specify username/password on user creation."""

    def create_user(**kwargs):
        user = user_factory.create(**kwargs)
        return user

    return create_user


@pytest.fixture
def philo_user(db, custom_user):
    """Dummy user who's thoughts can be updated by any authenticated user."""
    philo_username = f'philo{random.randint(10, 99)}'
    user = custom_user(username=philo_username)
    return user


@pytest.fixture
def thought_fix(db, thought_factory):
    return thought_factory()


@pytest.fixture
def custom_thought(db, thought_factory):
    """Object with the ability to accept custom field data."""

    def create_thought(**kwargs):
        thought = thought_factory.create(**kwargs)
        return thought

    return create_thought


@pytest.fixture
def custom_thought_batch(db, thought_factory):
    """Batch with the ability to accept custom field data."""

    def create_thought_batch(size, **kwargs):
        thought = thought_factory.create_batch(size, **kwargs)
        return thought

    return create_thought_batch


@pytest.fixture
def tag_fix(db, tag_factory):
    return tag_factory()


@pytest.fixture
def custom_tag(db, tag_factory):
    def create_tag(**kwargs):
        tag = tag_factory.create(**kwargs)
        return tag

    return create_tag


@pytest.fixture
def author_fix(db, author_factory):
    return author_factory()


@pytest.fixture
def api_rf():
    return APIRequestFactory()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_api_client(user):
    """Client for making authenticated requests."""
    client = APIClient()
    token = RefreshToken.for_user(user)
    access_token = str(token.access_token)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client


@pytest.fixture
def request_fix():
    def create_request(request):
        return Request(request)

    return create_request


@pytest.fixture
def sentence():
    return fake.sentence()


@pytest.fixture
def email_fix():
    return fake.email()


@pytest.fixture
def username_fix():
    return fake.user_name()


@pytest.fixture
def password_fix():
    return fake.password()
