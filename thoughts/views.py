import random

from django.conf import settings
from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import serializers, viewsets, generics, filters
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
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
from .utils import get_patterns


class ThoughtViewSet(viewsets.ModelViewSet):
    """A simple ViewSet to read, update, delete thoughts."""

    queryset = Thought.objects.all()
    serializer_class = ThoughtSerializer
    permission_classes = [IsOwnerOrFakeOrReadOnly, IsAuthenticatedOrReadOnly]
    pagination_class = CustomizedPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['text']

    def perform_create(self, serializer):
        """Save the user authorized with a token as an author."""
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=[
            'GET',
        ],
        permission_classes=[IsAuthenticated],
        url_path='my',
        url_name='my',
    )
    def my_thoughts(self, request):
        """List thoughts where an author is the authorized request user."""
        author = self.request.user
        thoughts = Thought.objects.filter(author=author).order_by('-id')
        paged_thoughts = self.paginate_queryset(thoughts)
        serializer = self.get_serializer(paged_thoughts, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=False,
        methods=[
            'GET',
        ],
        url_path='random',
        url_name='random',
    )
    def random(self, request):
        """Return a random thought be a real author."""
        thoughts = Thought.objects.filter(author__id__lte=20)
        random_thought = random.choice(thoughts)
        serializer = ThoughtSerializer(random_thought)
        return Response(serializer.data)


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
        authors = User.objects.annotate(thought_count=Count('thought'))
        return authors.filter(thought_count__gt=0).order_by('id')


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
        endpoints = []

        urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
        urlpatterns = urlconf.urlpatterns[1:]  # exclude admin

        for p in get_patterns(urlpatterns):
            pattern = ''.join(p).strip('$^')
            endpoints.append(f'{base}{pattern}')

        return Response(endpoints)
