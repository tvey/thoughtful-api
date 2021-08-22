from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Thought, User, Tag
from .serializers import (
    ThoughtSerializer,
    AuthorSerializer,
    AuthorDetailSerializer,
    TagSerializer,
    TagDetailSerializer,
)
from .permissions import IsOwnerOrFakeOrReadOnly
from .pagination import CustomizedPagination


class ThoughtViewSet(viewsets.ModelViewSet):
    """A simple ViewSet to read, update, delete thoughts."""

    queryset = Thought.objects.all()
    serializer_class = ThoughtSerializer
    permission_classes = [IsOwnerOrFakeOrReadOnly, IsAuthenticatedOrReadOnly]
    pagination_class = CustomizedPagination


class TagListAPIView(generics.ListAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class TagDetailAPIView(APIView):
    def get(self, request, pk=None, name=None, format=None):
        """Allow to access tag detail by id or by name"""
        lookup = {'name': name} if pk is None else {'pk': pk}
        tag = get_object_or_404(Tag, **lookup)
        serializer = TagDetailSerializer(tag, context={'request': request})
        return Response(serializer.data)


class AuthorListAPIView(generics.ListAPIView):
    serializer_class = AuthorSerializer
    pagination_class = None

    def get_queryset(self):
        """Return only authors who have thoughts."""
        qs = User.objects.annotate(thought_count=Count('thought'))
        return qs.filter(thought_count__gt=0).order_by('id')


class AuthorDetailAPIView(APIView):
    def get(self, request, pk=None, format=None):
        author = get_object_or_404(User, pk=pk)
        serializer = AuthorDetailSerializer(
            author, context={'request': request}
        )
        return Response(serializer.data)


class APIEndpoints(APIView):
    """List all available endpoints for the API."""

    def get(self, request):
        base = request.build_absolute_uri()

        endpoints = {
            'List thoughts': 'thoughts',
            'List authors': 'authors',
            'List tags': 'tags',
            'Create a thought': 'thoughts/new',
            'Thought detail': 'thoughts/<int:pk>',
            'Update a thought': 'thoughts/<int:pk>',
            'Delete a thought': 'thoughts/<int:pk>',
            'List thoughts by author id': 'authors/<int:pk>',
            'List thoughts by tag id': 'tags/<int:pk>',
            'List thoughts by tag name': 'tags/<str:name>',
        }

        for text, url in endpoints.items():
            endpoints[text] = f'{base}{url}'

        return Response(endpoints)
