import math

from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from django.db.models import CASCADE, PROTECT


class User(AbstractUser):

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Teacher(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    def __str__(self):
        return f"{self.name} {self.surname}"


class Product(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.OneToOneField(Teacher, on_delete=PROTECT)
    data_start = models.DateTimeField()
    price = models.FloatField()
    students = models.ManyToManyField('User', related_name='students', null=True, blank=True)  # По этому полю понимаем, есть ли доступ у студента к продукту
    min_students_in_group = models.PositiveIntegerField(default=1)
    max_students_in_group = models.PositiveIntegerField(default=3)

    def distribute_users_to_groups(self):
        eligible_users = self.students.all().prefetch_related('User')

        # Получаем всех пользователей, которые имеют доступ к продукту
        eligible_users = list(self.students.all())
        # Проверяем, начался ли уже продукт
        if self.data_start > timezone.now():
            sorted_users = sorted(eligible_users, key=lambda user: user.username)
        else:
            sorted_users = eligible_users

        # Распределяем пользователей по группам
        group_amount = math.ceil(len(sorted_users) / self.max_students_in_group)

        start_index = 0
        for i in range(group_amount):
            end_index = start_index + self.max_students_in_group
            if end_index < len(sorted_users):
                group_users = sorted_users[start_index:end_index]
            else:
                group_users = sorted_users[start_index:len(sorted_users)]

            group, created = Group.objects.get_or_create(product=self, name=f'Group {self.name} {i + 1}')
            group.students.set(group_users)

            start_index = end_index

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.distribute_users_to_groups()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Lesson(models.Model):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    video_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    students = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    # def clean(self):
    #     # Валидация на минимальное и максимальное количество учеников в группе
    #     if self.students.count() < self.product.min_students_in_group \
    #             or self.students.count() > self.product.max_students_in_group:
    #         raise ValidationError({'students': 'Недопустимое количество учеников в группе.'})

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
