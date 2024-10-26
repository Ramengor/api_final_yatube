"""Модуль настройки административной панели для моделей приложения."""
from django.contrib import admin

from posts.models import Comment, Follow, Group, Post


class PostsInline(admin.TabularInline):
    """Встроенное отображение постов в форме группы."""

    model = Post
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Настройки отображения модели Post в админке."""

    list_display = ('text', 'author', 'pub_date', 'group', 'image')
    search_fields = ('text',)
    list_filter = ('author', 'pub_date', 'group')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Настройки отображения модели Comment в админке."""

    list_display = ('author', 'post', 'text', 'created')
    search_fields = ('text', 'author__username')
    list_filter = ('created',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Настройки отображения модели Group в админке."""

    list_display = ('title', 'slug', 'description')
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'
    inlines = [PostsInline]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Настройки отображения модели Follow в админке."""

    list_display = ('id', 'user', 'following')
    search_fields = ('user__username', 'following__username')
    list_filter = ('user', 'following')
    empty_value_display = '-пусто-'
