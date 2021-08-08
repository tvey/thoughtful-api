from django.urls import path

from rest_framework import routers

from .views import ThoughtViewSet, list_tags, list_authors

urlpatterns = [
    path('tags/', list_tags, name='tags'),
    path('authors/', list_authors, name='authors'),
]

router = routers.SimpleRouter()
router.register(r'thoughts', ThoughtViewSet)
urlpatterns += router.urls
