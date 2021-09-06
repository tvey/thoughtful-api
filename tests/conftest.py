import random

import pytest
from faker import Faker
from pytest_factoryboy import register
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
    philo_username = f'philo{random.randint(1, 99)}'
    user = custom_user(username=philo_username)
    return user


@pytest.fixture
def custom_thought(db, thought_factory):
    def create_thought(**kwargs):
        thought = thought_factory.create(**kwargs)
        return thought

    return create_thought


@pytest.fixture
def custom_thought_batch(db, thought_factory):
    def create_thought_batch(size, **kwargs):
        thought = thought_factory.create_batch(size, **kwargs)
        return thought

    return create_thought_batch


@pytest.fixture
def api_rf():
    return APIRequestFactory()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_auth_client(user):
    client = APIClient()
    token = RefreshToken.for_user(user)
    access_token = str(token.access_token)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client


@pytest.fixture
def custom_api_auth_client(user):
    def create_client(user):
        client = APIClient()
        token = RefreshToken.for_user(user)
        access_token = str(token.access_token)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        return client

    return create_client


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
