from django.shortcuts import render
# Create your views here.

from django.shortcuts import render

from products.models import Product, ProductCategory

# Create your views here.
# функции = контроллер = представления = вьюшки/вьюхи


def index(request):
    context = {
        'title': 'GeekShop',
        'header': 'geekShop Store',
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'GeekShop - Каталог',
        'header': 'Создай свой образ в  GeekShop!',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'products/products.html', context)
