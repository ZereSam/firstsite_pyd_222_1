from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models


def get_min_length():
    min_length = 3
    return min_length


def validate_even(val):
    if val % 2 != 0:
        raise ValidationError('Число %(value)s нечетное', code='odd', params={'value': val})


# class MinMaxValueValidator:
#     def __init__(self, min_value, max_value):
#         self.min_value = min_value
#         self.max_value = max_value
#
#     def __call__(self, val):
#         if val < self.min_value or val > self.max_value:
#             raise ValidationError('Введенное число должно быть > %(min)s' 'и < %(max)s',
#                                   code='out_of_range',
#                                   params={'min': self.min_value,
#                                           'max': self.max_value})




# class Spare(models.Model):
#     name = models.CharField(max_length=30)
#
#
# class Machine(models.Model):
#     name = models.CharField(max_length=30)
#     spares = models.ManyToManyField(Spare)


class Rubric(models.Model):
    name = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name="Название",
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Выполняем какие-то действия
        if True:
            super().save(*args, **kwargs)
        # Выполняем какие-то действия после сохранения

    def delete(self, *args, **kwargs):
        # Выполняем какие-то действия
        if True:
            super().delete(*args, **kwargs)
        # Выполняем какие-то действия после

    def get_absolute_url(self):
        #return "/bboard/%s/" % self.pk
        #return f"/bboard/{self.pk}/"
        return f"/{self.pk}/"

    def title_and_price(self):
        if self.price:
            #return '%s (%.2f)' % (self.title, self.price)
            return f'{self.title} ({self.price:.2f})'
        return self.title

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['name']
        #ordering = ['-published', 'title']


class Bb(models.Model):
    KINDS = {
        ('b', 'Куплю'),
        ('s', 'Продам'),
        ('c', 'Поменяю'),
    }

    rubric = models.ForeignKey(
        'Rubric',
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
    )

    title = models.CharField(
        max_length=50,
        verbose_name="Товар",
        validators=[validators.MinLengthValidator(get_min_length)],
        #validators=[validators.RegexValidator(regex='^.{4,}$', inverse_match=True)]
        error_messages={'min_length': 'Слишком много символов'},
    )

    kind = models.CharField(
        max_length=1,
        choices=KINDS,
        default='s'
    )

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание",
    )

    price = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Цена",
        validators=[validate_even, #MinMaxValueValidator(50, 60_000_000)
         ]
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Опубликовано",
    )

    def __str__(self):
        return f'Объявление: {self.title}'

    class Meta:
        #order_with_respect_to = 'rubric'
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-published', 'title']
        #db_table = 'bboard_bb'

# class Person(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     age = models.IntegerField()
#     email = models.EmailField()
#     phone_number = models.CharField(max_length=10)
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"
#
#
# class Child(models.Model):
#     parent = models.ForeignKey("Person", on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100)
#     age = models.IntegerField()
#     favorite_ise_cream = models.ForeignKey("")
#
#     def __str__(self):
#         return f"{self.first_name}"
#
# class IceCream(models.Model):
#     FLAVORS_CHOICES = (
#         ('V', 'Ваниль'),
#         ('C', 'Шоколад'),
#         ('S', 'Клубника'),
#         ('P', 'Пломбир'),
#     )
#
#     name = models.CharField(max_length=100)
#     flavor = models.CharField(max_length=1, choices=FLAVORS_CHOICES)
#     price = models.DecimalField(max_digits=1, decimal_places=2)
#
#
