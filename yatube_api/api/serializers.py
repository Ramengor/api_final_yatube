"""Модуль для сериализации моделей API."""
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Post, Comment, Group, Follow


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        """Метаданные для сериализатора Post."""

        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        """Метаданные для сериализатора Comment."""

        fields = '__all__'
        model = Comment
        read_only_fields = ['author', 'post']


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        """Метаданные для сериализатора Group."""

        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow."""

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())

    class Meta:
        """Метаданные для сериализатора Follow."""

        model = Follow
        fields = '__all__'

    def validate(self, attrs):
        """Проверяет, что пользователь не подписывается на самого себя."""
        user = self.context['request'].user
        following = attrs['following']
        if user == following:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя.")

        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого пользователя.")
        return attrs
