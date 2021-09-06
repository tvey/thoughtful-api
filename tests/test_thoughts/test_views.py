import random
from thoughts.models import Thought

import pytest

from django.urls import reverse

from thoughts.models import Thought

pytestmark = [pytest.mark.django_db]


class TestThoughtEndpoints:
    overview_url = reverse('overview')
    thought_base_url = reverse('thought-list')
    my_list_url = reverse('thought-my')
    batch_size = 3
    rand_obj_index = random.randrange(batch_size)

    def test_thought_list_no_objects(self, api_client):
        response = api_client.get(self.thought_base_url)
        data = response.json()
        assert response.status_code == 200
        assert data['results'] == []
        assert data['meta']['total_items'] == 0

    def test_thought_list_returns_existing_objects(
        self, api_client, thought_factory
    ):
        thought_factory.create_batch(self.batch_size)
        response = api_client.get(self.thought_base_url)
        data = response.json()
        assert response.status_code == 200
        assert len(data['results']) == self.batch_size
        assert data['meta']['total_items'] == self.batch_size

    def test_my_thought_list_authenticated_user_no_objects(
        self, api_auth_client
    ):
        response = api_auth_client.get(self.my_list_url)
        data = response.json()
        assert response.status_code == 200
        assert data['results'] == []
        assert not data['meta']['total_items']

    def test_my_thought_list_authenticated_user_with_objects(
        self, user, custom_api_auth_client, custom_thought_batch
    ):
        custom_thought_batch(self.batch_size, author=user)
        response = custom_api_auth_client(user).get(self.my_list_url)
        data = response.json()
        rand_obj = data['results'][self.rand_obj_index]
        assert response.status_code == 200
        assert len(data['results']) == self.batch_size
        assert data['meta']['total_items'] == self.batch_size
        assert rand_obj['author'] == user.username

    def test_my_thought_list_unauthenticated_user(self, api_client):
        response = api_client.get(self.my_list_url)
        assert response.status_code == 403
        msg = 'Authentication credentials were not provided.'
        assert response.json()['detail'] == msg

    def test_create_thought_authenticated_user(
        self, user, sentence, custom_api_auth_client
    ):
        data = {'text': sentence}
        api_client = custom_api_auth_client(user)
        response = api_client.post(self.thought_base_url, data=data)
        assert response.status_code == 201
        assert Thought.objects.count() == 1
        assert response.json()['text'] == sentence
        assert response.json()['author'] == user.username

    def test_create_thought_unauthenticated_user(self, api_auth_client):
        ...

    def test_retrieve_thought(self, custom_thought, user, sentence, api_client):
        thought = custom_thought(text=sentence, author=user)
        url = reverse('thought-detail', kwargs={'pk': thought.id})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.json()['text'] == sentence
        assert response.json()['author'] == user.username

    def test_retrieve_thought_not_found(self, api_client):
        url = reverse('thought-detail', kwargs={'pk': random.randint(0, 999)})
        response = api_client.get(url)
        assert response.status_code == 404

    def test_update_thought_authenticated_user_and_author(self, api_client):
        ...

    def test_update_thought_authenticated_user_not_author(
        self, api_auth_client
    ):
        ...

    def test_update_thought_unauthenticated_user(self, api_client):
        ...

    def test_partial_update(self, api_client):
        ...

    def test_delete(self, mocker, api_client):
        ...


class TestTagEndpoints:
    # list
    # detail
    pass


class TestAuthorEndpoints:
    pass


@pytest.mark.skip
def test_testing_to_testify_tests(
    user_factory,
    tag_factory,
    thought_factory,
    custom_thought,
    user,
    custom_user,
    api_client,
    api_auth_client,
    api_rf,
):
    cu = custom_user(username='zaphod')
    ct = custom_thought(text='Be nice', author=cu)
    four_thoughts = thought_factory.create_batch(4)
    base_url = reverse('overview')
    r1 = api_client.get(base_url)
    r2 = api_auth_client.get(base_url)
    assert user.username and user.password
    assert ct.author.username == cu.username
    assert r1.status_code == 200
    assert r2.status_code == 200
