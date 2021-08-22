import re

from rest_framework import serializers

from .models import Thought, Tag, User


class ThoughtSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Thought
        fields = ['id', 'text', 'author', 'is_editable', 'tags']


class AuthorSerializer(serializers.ModelSerializer):
    thought_count = serializers.SerializerMethodField(read_only=True)
    detail = serializers.HyperlinkedIdentityField(
        view_name='author-detail',
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'thought_count', 'detail']

    def get_thought_count(self, obj):
        return Thought.objects.filter(author=obj).count()


class AuthorDetailSerializer(AuthorSerializer):
    thought_ids = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'thought_count', 'thought_ids']

    def get_thought_ids(self, obj):
        return obj.thought_set.values_list('id', flat=True)


class TagSerializer(serializers.ModelSerializer):
    thought_count = serializers.SerializerMethodField(read_only=True)
    detail = serializers.HyperlinkedIdentityField(
        view_name='tag-detail-name',
        lookup_field='name',
    )

    class Meta:
        model = Tag
        fields = ['id', 'name', 'thought_count', 'detail']

    def get_thought_count(self, obj):
        return Thought.objects.filter(tags__in=[obj.id]).count()


class TagDetailSerializer(TagSerializer):
    thought_ids = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'thought_count', 'thought_ids']

    def get_thought_ids(self, obj):
        qs = Thought.objects.filter(tags__in=[obj.id])
        return qs.values_list('id', flat=True)
