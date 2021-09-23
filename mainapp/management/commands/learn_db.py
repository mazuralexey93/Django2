from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from django.db.models import Q


class Command(BaseCommand):
   def handle(self, *args, **options):
       test_products = Product.objects.filter(
           Q(category__name='Дом') |
           Q(category__name='Офис')
       )
       print(len(test_products))
       print(test_products)
