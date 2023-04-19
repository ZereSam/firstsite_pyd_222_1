from django.db import models


class Bb(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Товар'
    )

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    price = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Цена'
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опубликовано'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявление"
        ordering = ['-published']