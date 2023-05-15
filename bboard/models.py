from django.contrib.auth.models import User
from django.db import models


class AdvUser(models.Model):
    is_activated = models.BooleanField(
        default=True,
    )

    user = models.OneToOneField(
        User,
        on_delete=True,
    )


class Spare(models.Model):
    name = models.CharField(max_length=30)


class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare)


class Rubric(models.Model):
    name = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name="Название",
        help_text="Опубликовано"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['name']





class Bb(models.Model):
    rubric = models.ForeignKey(
        'Rubric',
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
    )

    title = models.CharField(
        max_length=50,
        verbose_name="Товар",
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
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Опубликовано",
    )

    def __str__(self):
        return f'Объявление: {self.title}'

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-published', 'title']
      db_table = 'bboard_bb'

    class Person(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        age = models.IntegerField()
        email = models.EmailField()
        phone_number = models.CharField(max_length=10)

        def __str__(self):
            return f"{self.first_name} {self.last_name}"


    class Child(models.Model):
        parent = models.ForeignKey("Person", on_delete=models.CASCADE)
        first_name = models.CharField(max_length=100)
        age = models.IntegerField()
        favorite_ise_cream = models.ForeignKey("")

        def __str__(self):
            return f"{self.first_name}"

    class IceCream(models.Model):
        FLAVORS_CHOICES = (
            ('V', 'Ваниль'),
            ('C', 'Шоколад'),
            ('S', 'Клубника'),
            ('P', 'Пломбир'),
        )

        name = models.CharField(max_length=100)
        flavor = models.CharField(max_length=1, choices=FLAVORS_CHOICES)
        price = models.DecimalField(max_digits=1, decimal_places=2)


