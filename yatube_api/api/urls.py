"""Модуль для определения URL-адресов API."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet)

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register('follow', FollowViewSet, basename='follow')
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comments'
                )

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
