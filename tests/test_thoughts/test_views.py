import random

import pytest

from django.urls import reverse
from django.conf import settings

from thoughts.models import Thought
from thoughts.utils import get_patterns as get_patterns_util

pytestmark = [pytest.mark.django_db(transaction=True)]


class TestThoughtEndpoints:
    overview_url = reverse('overview')
    thought_base_url = reverse('thought-list')
    my_list_url = reverse('thought-my')
    random_thought_url = reverse('thought-random')
    batch_size = random.randint(2, 10)
    rand_obj_index = random.randrange(batch_size)
    no_credentials_msg = 'Authentication credentials were not provided.'
    no_permission_msg = 'You do not have permission to perform this action.'

    def test_thought_list_no_objects(self, api_client):
        response = api_client.get(self.thought_base_url)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data.get('results') == []
        assert response_data.get('meta').get('total_items') == 0

    def test_thought_list_returns_existing_objects(
        self, api_client, thought_factory
    ):
        thought_factory.create_batch(self.batch_size)
        response = api_client.get(self.thought_base_url)
        response_data = response.json()
        assert response.status_code == 200
        assert len(response_data.get('results')) == self.batch_size
        assert response_data.get('meta').get('total_items') == self.batch_size

    def test_my_thought_list_authenticated_user_no_objects(
        self, auth_api_client
    ):
        response = auth_api_client.get(self.my_list_url)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data.get('results') == []
        assert response_data.get('meta').get('total_items') == 0

    def test_my_thought_list_authenticated_user_with_objects(
        self, user, auth_api_client, custom_thought_batch
    ):
        custom_thought_batch(self.batch_size, author=user)
        response = auth_api_client.get(self.my_list_url)
        response_data = response.json()
        rand_obj = response_data.get('results')[self.rand_obj_index]
        assert response.status_code == 200
        assert len(response_data.get('results')) == self.batch_size
        assert response_data.get('meta').get('total_items') == self.batch_size
        assert rand_obj.get('author') == user.username

    def test_my_thought_list_unauthenticated_user(self, api_client):
        response = api_client.get(self.my_list_url)
        assert response.status_code == 403
        assert response.json().get('detail') == self.no_credentials_msg

    def test_random_endpoint_returns_valid_result(
        self, api_client, custom_thought_batch
    ):
        custom_thought_batch(self.batch_size)
        response = api_client.get(self.random_thought_url)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data.get('text')
        assert response_data.get('author')

    def test_create_thought_authenticated_user(
        self, user, sentence, auth_api_client
    ):
        payload = {'text': sentence}
        response = auth_api_client.post(self.thought_base_url, data=payload)
        assert response.status_code == 201
        assert Thought.objects.count() == 1
        assert response.json().get('text') == sentence
        assert response.json().get('author') == user.username

    def test_create_thought_unauthenticated_user(self, sentence, api_client):
        response = api_client.post(
            self.thought_base_url, data={'text': sentence}
        )
        assert response.status_code == 403
        assert response.json().get('detail') == self.no_credentials_msg

    def test_perform_create(self, user, sentence, auth_api_client):
        payload = {'text': sentence}
        response = auth_api_client.post(self.thought_base_url, data=payload)
        assert response.json().get('author') == user.username

    def test_retrieve_thought(self, custom_thought, user, sentence, api_client):
        thought = custom_thought(text=sentence, author=user)
        url = reverse('thought-detail', kwargs={'pk': thought.id})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.json().get('text') == sentence
        assert response.json().get('author') == user.username

    def test_retrieve_thought_not_found(self, api_client):
        url = reverse('thought-detail', kwargs={'pk': random.randint(0, 999)})
        response = api_client.get(url)
        assert response.status_code == 404

    def test_update_thought_authenticated_user_and_author(
        self, user, custom_thought, sentence, auth_api_client
    ):
        thought = custom_thought(author=user, text=sentence)
        url = reverse('thought-detail', kwargs={'pk': thought.id})
        change = '123'
        payload = {
            'text': f'{sentence} {change}',
            'is_editable': not thought.is_editable,
        }
        response = auth_api_client.put(url, data=payload)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data.get('text').endswith(change)
        assert response_data.get('id') == thought.id
        assert response_data.get('author') == user.username
        assert response_data.get('is_editable') != thought.is_editable

    def test_update_thought_authenticated_user_not_author(
        self,
        custom_user,
        custom_thought,
        username_fix,
        sentence,
        auth_api_client,
    ):
        other_user = custom_user(username=username_fix)
        thought = custom_thought(author=other_user, text=sentence)
        url = reverse('thought-detail', kwargs={'pk': thought.id})
        response = auth_api_client.put(url, data={'text': f'{sentence} 123'})
        response_data = response.json()
        assert thought.author == other_user
        assert response.status_code == 403
        assert response_data.get('detail') == self.no_permission_msg
        assert response_data.get('author') is None
        assert response_data.get('text') is None

    def test_update_thought_unauthenticated_user(self, thought, api_client):
        url = reverse('thought-detail', kwargs={'pk': thought.id})
        response = api_client.put(url, data={'text': '123'})
        assert response.status_code == 403
        assert response.json().get('detail') == self.no_credentials_msg
        assert 'text' not in response.json()

    def test_authenticated_user_can_update_philo_user_thought(
        self, user, philo_user, custom_thought, api_client
    ):
        """Test authenticated users can update thoughts of fake (philo) users."""
        thought = custom_thought(author=philo_user)
        url = reverse('thought-detail', kwargs={'pk': thought.id})
        api_client.force_authenticate(user=user)
        response = api_client.put(url, data={'text': '123'})
        response_data = response.json()
        assert thought.author == philo_user
        assert response.status_code == 200
        assert response_data.get('author') != user.username
        assert response_data.get('author') == philo_user.username
        assert response_data.get('text') == '123'

    def test_unauthenticated_user_cannot_update_philo_user_thought(
        self, philo_user, custom_thought, api_client
    ):
        thought = custom_thought(author=philo_user)
        url = reverse('thought-detail', kwargs={'pk': thought.id})
        response = api_client.put(url, data={'text': '123'})
        assert thought.author == philo_user
        assert response.status_code == 403
        assert response.json().get('detail') == self.no_credentials_msg

    def test_delete_thought_authenticated_user_and_author(
        self, user, custom_thought, auth_api_client
    ):
        thought = custom_thought(author=user)
        url = reverse('thought-detail', kwargs={'pk': thought.id})
        response = auth_api_client.delete(url)
        assert thought.author == user
        assert response.status_code == 204

    def test_delete_thought_authenticated_user_not_author(
        self, custom_user, custom_thought, username_fix, auth_api_client
    ):
        other_user = custom_user(username=username_fix)
        thought = custom_thought(author=other_user)
        url = reverse('thought-detail', kwargs={'pk': thought.id})
        response = auth_api_client.delete(url)
        assert thought.author == other_user
        assert response.status_code == 403
        assert response.json().get('detail') == self.no_permission_msg

    def test_delete_thought_unauthenticated_user(self, thought_fix, api_client):
        url = reverse('thought-detail', kwargs={'pk': thought_fix.id})
        response = api_client.delete(url)
        assert response.status_code == 403
        assert response.json().get('detail') == self.no_credentials_msg

    def test_paginated_thought_response(self, thought_factory, api_client):
        bigger_batch = 51
        thought_factory.create_batch(bigger_batch)
        response = api_client.get(self.thought_base_url)
        response_data = response.json()
        expected_page_size = settings.REST_FRAMEWORK.get('PAGE_SIZE')
        assert response.status_code == 200
        assert len(response_data.get('results')) == expected_page_size


class TestTagEndpoints:
    tag_base_url = reverse('tags')
    batch_size = 10
    rand_obj_index = random.randrange(batch_size)

    def test_tag_list(self, tag_factory, api_client):
        tags = tag_factory.create_batch(self.batch_size)
        response = api_client.get(self.tag_base_url)
        response_data = response.json()
        rand_obj = response_data[self.rand_obj_index]
        assert response.status_code == 200
        assert len(response_data) == self.batch_size
        assert [t.name for t in tags] == [t.get('name') for t in response_data]
        assert 'id' in rand_obj
        assert 'name' in rand_obj
        assert 'detail' in rand_obj
        assert 'thought_count' in rand_obj

    def test_tag_detail_by_pk(self, tag_fix, api_client):
        url = reverse('tag-detail-pk', kwargs={'pk': tag_fix.id})
        response = api_client.get(url)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data.get('id') == tag_fix.id
        assert response_data.get('name') == tag_fix.name
        assert 'thought_ids' in response_data
        assert 'thought_count' in response_data

    def test_tag_detail_by_name(self, tag_fix, api_client):
        url = reverse('tag-detail-name', kwargs={'name': tag_fix.name})
        response = api_client.get(url)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data.get('id') == tag_fix.id
        assert response_data.get('name') == tag_fix.name
        assert 'thought_ids' in response_data
        assert 'thought_count' in response_data

    def test_tag_detail_not_found(self, api_client):
        url_1 = reverse('tag-detail-pk', kwargs={'pk': 42})
        response_1 = api_client.get(url_1)
        url_2 = reverse('tag-detail-name', kwargs={'name': 'everything'})
        response_2 = api_client.get(url_2)
        assert response_1.status_code == 404
        assert response_2.status_code == 404


class TestAuthorEndpoints:
    def test_user_without_thought_not_in_authors(
        self,
        user_factory,
        user,
        custom_thought,
        api_client,
    ):
        batch_size = 10
        authors = user_factory.create_batch(batch_size)

        for author in authors:
            custom_thought(author=author)

        response = api_client.get(reverse('authors'))
        response_data = response.json()
        assert response.status_code == 200
        assert len(response_data) == batch_size
        author_usernames = [i.get('username') for i in response_data]
        assert user.username not in author_usernames

    def test_author_list_expected_field(self, user, custom_thought, api_client):
        custom_thought(author=user)  # thoughts are required to be an author
        response = api_client.get(reverse('authors'))
        assert response.status_code == 200
        assert len(response.json()) == 1
        author_data = response.json()[0]
        assert author_data.get('id') == user.id
        assert author_data.get('username') == user.username
        assert author_data.get('thought_count') == 1
        assert author_data.get('detail')

    def test_author_detail(self, user, custom_thought, api_client):
        custom_thought(author=user)
        url = reverse('author-detail', kwargs={'pk': user.id})
        response = api_client.get(url)
        response_data = response.json()
        assert response.status_code == 200
        assert 'id' in response_data
        assert 'username' in response_data
        assert 'thought_count' in response_data
        assert 'thought_ids' in response_data
        assert response_data.get('thought_count') == 1

    def test_author_detail_not_found(self, api_client):
        url = reverse('author-detail', kwargs={'pk': 123})
        response = api_client.get(url)
        assert response.status_code == 404


class TestOverview:
    url = reverse('overview')

    def test_get_urlpatterns_with_bad_data(self):
        patters = ['abc', 123]
        assert not list(get_patterns_util(patters))
