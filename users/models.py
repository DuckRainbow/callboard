from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    first_name = models.CharField(
        max_length=25,
        verbose_name='имя пользователя',
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=25,
        verbose_name='фамилия пользователя',
        blank=True,
        null=True,
    )

    email = models.EmailField(
        unique=True,
        verbose_name='электронная почта пользователя'
    )

    token = models.CharField(
        max_length=100,
        verbose_name='Token',
        blank=True,
        null=True,
    )

    phone_num = models.CharField(
        max_length=12,
        verbose_name='телефон для связи',
        blank=True,
        null=True,
    )
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(
        choices=ROLE_CHOICES,
        default='user',
    )

    image = models.ImageField(
        verbose_name='аватарка пользователя',
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
