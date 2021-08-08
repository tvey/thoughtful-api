from rest_framework import serializers

from .models import Thought, Tag, User


class AuthorSerializer(serializers.ModelSerializer):
    thought_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'thought_count']

    def get_thought_count(self, obj):
        return Thought.objects.filter(author=obj).count()


class TagSerializer(serializers.ModelSerializer):
    thought_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'thought_count']

    def get_thought_count(self, obj):
        return Thought.objects.filter(tags__in=[obj.id]).count()


class ThoughtSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Thought
        fields = ['id', 'text', 'author', 'tags']
