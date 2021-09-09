import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from users.serializers import RegisterSerializer

pytestmark = [pytest.mark.django_db(transaction=True)]


class TestRegisterSerializer:
    serializer = RegisterSerializer

    def test_password_validation_with_invalid_data(
        self, username_fix, password_fix
    ):
        data = {
            'username': username_fix,
            'password': password_fix,
            'password2': password_fix + '123',
        }
        assert not self.serializer(data=data).is_valid()

    def test_password_validation_with_valid_data(
        self, username_fix, password_fix
    ):
        data = {
            'username': username_fix,
            'password': password_fix,
            'password2': password_fix,
        }
        assert self.serializer(data=data).is_valid()

    def test_create(self, username_fix, password_fix, request_fix, api_rf):
        data = {
            'username': username_fix,
            'password': password_fix,
            'password2': password_fix,
        }
        request = api_rf.post(reverse('users:register'))
        serializer_context = {'request': request_fix(request)}
        serializer = self.serializer(data=data, context=serializer_context)
        assert serializer.is_valid()
        if serializer.is_valid():
            serializer.save()

        User = get_user_model()
        assert User.objects.filter(username=username_fix).exists()
