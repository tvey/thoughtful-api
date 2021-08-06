from rest_framework import serializers

from .models import Thought, Tag, User


class UserSerializer(serializers.ModelSerializer):
    thought_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'thought_count']

    def get_thought_count(self, obj):
        return Thought.objects.filter(author=obj).count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ThoughtSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Thought
        fields = ['id', 'text', 'author', 'tags']
