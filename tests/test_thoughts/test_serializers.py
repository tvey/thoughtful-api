from django.urls import reverse

from thoughts.serializers import (
    ThoughtSerializer,
    TagSerializer,
    TagDetailSerializer,
    AuthorSerializer,
    AuthorDetailSerializer,
)


class TestThoughtSerializer:
    serializer = ThoughtSerializer

    def test_serializer_returns_expected_fields(self, thought_fix):
        data = self.serializer(thought_fix).data
        expected = {'id', 'text', 'author', 'is_editable', 'tags'}
        assert data.keys() & expected == expected

    def test_thought_tags_string_related(self, custom_thought, tag_factory):
        tags = tag_factory.create_batch(3)
        thought = custom_thought(tags=tags)
        tag_names = [t.name for t in tags]
        data = self.serializer(thought).data
        assert list(data.get('tags')) == tag_names

    def test_thought_author_string_related(self, custom_thought, user):
        thought = custom_thought(author=user)
        data = self.serializer(thought).data
        assert data.get('author') == user.username


class TestTagSerializer:
    serializer = TagSerializer

    def test_tag_thought_count(
        self, tag_factory, custom_thought_batch, api_rf, request_fix
    ):
        tag = tag_factory()
        batch_size = 10
        custom_thought_batch(batch_size, tags=[tag])
        request = api_rf.get(reverse('tag-detail-pk', kwargs={'pk': tag.id}))
        serializer_context = {'request': request_fix(request)}
        data = self.serializer(tag, context=serializer_context).data
        assert data.get('thought_count') == batch_size


class TestTagDetailSerializer:
    serializer = TagDetailSerializer

    def test_tag_thought_ids_list(self, tag_factory, custom_thought_batch):
        tag = tag_factory()
        batch_size = 10
        thoughts = custom_thought_batch(batch_size, tags=[tag])
        thought_ids = [t.id for t in thoughts]
        data = self.serializer(tag).data
        serialized_thought_ids = data.get('thought_ids')
        assert list(serialized_thought_ids) == thought_ids
        assert len(serialized_thought_ids) == batch_size


class TestAuthorSerializer:
    serializer = AuthorSerializer

    def test_tag_thought_count(
        self, user, custom_thought_batch, api_rf, request_fix
    ):
        batch_size = 10
        custom_thought_batch(batch_size, author=user)
        request = api_rf.get(reverse('author-detail', kwargs={'pk': user.id}))
        serializer_context = {'request': request_fix(request)}
        data = self.serializer(user, context=serializer_context).data
        assert data.get('thought_count') == batch_size


class TestAuthorDetailSerializer:
    serializer = AuthorDetailSerializer

    def test_author_thought_ids_list(self, user, custom_thought_batch):
        batch_size = 10
        thoughts = custom_thought_batch(batch_size, author=user)
        thought_ids = [t.id for t in thoughts]
        data = self.serializer(user).data
        serialized_thought_ids = data.get('thought_ids')
        assert list(serialized_thought_ids) == thought_ids
        assert len(serialized_thought_ids) == batch_size
