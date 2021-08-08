from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Thought, User, Tag
from .serializers import ThoughtSerializer, TagSerializer, AuthorSerializer


class ThoughtViewSet(viewsets.ModelViewSet):
    """A simple ViewSet for viewing and editing thoughts."""

    queryset = Thought.objects.all()
    serializer_class = ThoughtSerializer


@api_view(['GET'])
def list_tags(request):
    serializer = TagSerializer(Tag.objects.all(), many=True)
    return Response({'tags': serializer.data})


@api_view(['GET'])
def list_authors(request):
    serializer = AuthorSerializer(User.objects.all(), many=True)
    return Response({'authors': serializer.data})


# To-do: add users views and permissions, add and customize actions
