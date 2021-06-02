from django.db import models


# Create your models here. == таблицы
class ProductCategory(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField(blank=True)
