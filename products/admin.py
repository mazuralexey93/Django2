from django.contrib import admin

from products.models import ProductCategory, Product

# Register your models here. == добавление таблиц в админку

admin.site.register(Product)
admin.site.register(ProductCategory)
