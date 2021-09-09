import pytest

from django.db import IntegrityError


class TestTagModel:
    def test_tag_name_is_unique(self, tag_fix, custom_tag):
        with pytest.raises(IntegrityError):
            custom_tag(name=tag_fix.name)

    def test_tag_str(self, tag_fix):
        assert str(tag_fix) == tag_fix.name


class TestThoughtModel:
    def test_thought_str(self, thought_fix):
        expected = f'Thought {thought_fix.id} by {thought_fix.author.username}'
        assert str(thought_fix) == expected
