"""Модуль, содержащий модели приложения Posts."""
from django.contrib.auth import get_user_model
from django.db import models

from posts.constants import TITLE_LENGTH

User = get_user_model()


class Group(models.Model):
    """Модель группы."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        """Метаданные модели группы."""

        ordering = ['title']

    def __str__(self):
        """Возвращает название группы."""
        return self.title[:TITLE_LENGTH]


class Post(models.Model):
    """Модель поста.

    Посты содержащие текст, дату публикации, автора,
    изображение и группу.
    """

    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts')
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )

    class Meta:
        """Метаданные модели поста."""

        ordering = ['-pub_date']

    def __str__(self):
        """Возвращает текст поста."""
        return self.text[:TITLE_LENGTH]


class Comment(models.Model):
    """Модель комментария."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True)

    class Meta:
        """Метаданные модели комментария."""

        ordering = ['-created']

    def __str__(self):
        """Возвращает строку с информацией о комментарии."""
        return (f'Комментарий от {self.author} на {self.post} '
                f'- {self.text[:TITLE_LENGTH]}')


class Follow(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower')
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following')

    class Meta:
        """Метаданные модели подписки."""

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='prevent_unique_follow'
            )
        ]

    def __str__(self):
        """Возвращает строку с информацией о подписке."""
        return f'{self.user} follows {self.following}'
