"""Модуль представлений API."""
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet


from posts.models import Post, Group, Follow
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer,)
from api.permissions import IsAuthorOrReadOnly
from api.pagination import PostPagination


class PostViewSet(viewsets.ModelViewSet):
    """Представление для управления постами."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]

    pagination_class = PostPagination

    def perform_create(self, serializer):
        """Сохраняет пост с автором текущего пользователя."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для управления комментариями."""

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]
    pagination_class = None

    def get_post(self):
        """Получает пост по ID из параметров URL."""
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        """Возвращает все комментарии для заданного поста."""
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        """Сохраняет комментарий с автором и привязывает его к посту."""
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(ReadOnlyModelViewSet):
    """Представление для управления группами."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class FollowViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    GenericViewSet):
    """Представление для управления подписками пользователей."""

    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        """Возвращает подписки текущего пользователя, с возможностью поиска."""
        queryset = Follow.objects.filter(user=self.request.user)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(following__username__icontains=search)
        return queryset

    def perform_create(self, serializer):
        """Сохраняет подписку с текущим пользователем."""
        serializer.save(user=self.request.user)
