from django.db import models
from django.db.models.aggregates import Count
from random import randint


class CategoryManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class Category(models.Model):
    name = models.CharField(max_length=50)
    objects = CategoryManager()

    def __str__(self):
        return self.name


class Drawing(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    time = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='self.name/')

    def __str__(self):
        return self.category


class TempCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
