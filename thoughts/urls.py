from django.urls import path

from rest_framework import routers

from .views import (
    ThoughtViewSet,
    AuthorListAPIView,
    AuthorDetailAPIView,
    TagListAPIView,
    TagDetailAPIView,
    APIEndpoints,
)

urlpatterns = [
    path('', APIEndpoints.as_view(), name='overview'),
    path('authors/', AuthorListAPIView.as_view(), name='authors'),
    path('authors/<int:pk>', AuthorDetailAPIView.as_view(), name='author-detail'),
    path('tags/', TagListAPIView.as_view(), name='tags'),
    path('tags/<int:pk>', TagDetailAPIView.as_view(), name='tag-detail-pk'),
    path('tags/<str:name>', TagDetailAPIView.as_view(), name='tag-detail-name'),
]

router = routers.SimpleRouter()
router.register(r'thoughts', ThoughtViewSet)
urlpatterns += router.urls
