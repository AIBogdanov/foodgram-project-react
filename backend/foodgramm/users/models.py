
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]
    email = models.EmailField(
        'e-mail address',
        max_length=200,
        unique=True,
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписки на автора."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'], name='uniq_couple')
        ]

    def __str__(self):
        return self.username
