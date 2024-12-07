from django.db import models

from users.models import User


class Ad(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Название товара',
        blank=True,
        null=True,
        help_text='Введите название товара',
    ),

    price = models.IntegerField(
        verbose_name='Стоимость',
        blank=True,
        null=True,
        help_text='Введите стоимость товара',
    ),

    description = models.CharField(
        max_length=50,
        verbose_name='Описание',
        blank=True,
        null=True,
        help_text='Опишите товар',
    ),

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    ),

    created_at = models.DateTimeField(
        verbose_name='Дата создания объявления',
        blank=True,
        null=True,
    ),

    def __str__(self):
        # Строковое отображение объекта
        return (
            f"Товар {self.title}, стоимость {self.price}"
        )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Review(models.Model):
    text = models.CharField(
        max_length=50,
        verbose_name='Текст отзыва',
        blank=True,
        null=True,
        help_text='Введите текст отзыва',

    ),

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    ),

    ad = models.ForeignKey(
        User,
        verbose_name='Объявление',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    ),

    created_at = models.DateTimeField(
        verbose_name='Дата создания объявления',
        blank=True,
        null=True,
    ),

    def __str__(self):
        # Строковое отображение объекта
        return (
            f"Отзыв {self.author} к {self.ad}:  {self.text}. {self.created_at}"
        )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
