import pytest

from django.urls import reverse

pytestmark = [pytest.mark.django_db(transaction=True)]


class TestUserEndpoints:
    def test_register_with_valid_data(
        self, username_fix, password_fix, api_client
    ):
        payload = {
            'username': username_fix,
            'password': password_fix,
            'password2': password_fix,
        }
        url = reverse('users:register')
        response = api_client.post(url, data=payload)
        assert response.status_code == 200
        assert 'User created' in response.json().get('message')
        assert response.json().get('username') == username_fix

    def test_register_with_invalid_data(
        self, username_fix, password_fix, api_client
    ):
        payload = {
            'username': username_fix,
            'password': password_fix,
            'password2': password_fix + '123',
        }
        url = reverse('users:register')
        response = api_client.post(url, data=payload)
        assert response.status_code == 400
        assert response.json().get('password')

    def test_obtain_token(self, user, password_fix, api_client):
        user.set_password(password_fix)
        user.save()
        url = reverse('users:token_obtain_pair')
        payload = {'username': user.username, 'password': password_fix}
        response = api_client.post(url, data=payload)
        assert response.status_code == 200
        assert response.json().get('access')
        assert response.json().get('refresh')

    def test_refresh_token(self, user, password_fix, api_client):
        user.set_password(password_fix)
        user.save()
        obtain_url = reverse('users:token_obtain_pair')
        payload = {'username': user.username, 'password': password_fix}
        obtain_response = api_client.post(obtain_url, data=payload)
        refresh_token = obtain_response.json().get('refresh')
        refresh_url = reverse('users:token_refresh')
        response = api_client.post(refresh_url, data={'refresh': refresh_token})
        assert response.status_code == 200
        assert response.json().get('access')

    def test_obtain_token_unauthorized(
        self, username_fix, password_fix, api_client
    ):
        url = reverse('users:token_obtain_pair')
        payload = {'username': username_fix, 'password': password_fix}
        response = api_client.post(url, data=payload)
        msg = 'No active account found with the given credentials'
        assert response.status_code == 401
        assert response.json().get('detail') == msg

    def test_obtain_token_bad_data(self, api_client):
        url = reverse('users:token_obtain_pair')
        response = api_client.post(url, data={})
        required = ['This field is required.']
        assert response.status_code == 400
        assert response.json().get('username') == required
        assert response.json().get('password') == required
