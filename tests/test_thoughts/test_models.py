import pytest

pytestmark = pytest.mark.django_db


class TestTest:
    def test_happy(self):
        assert 'Yeah'
