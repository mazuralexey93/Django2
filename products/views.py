from django.shortcuts import render
# Create your views here.

from django.shortcuts import render

from products.models import Product, ProductCategory

# Create your views here.
# функции = контроллер = представления = вьюшки/вьюхи


def index(request):
    context = {
        'title': 'GeekShop',
        'header': 'GeekShop Store',
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None):
    context = {
        'title': 'GeekShop - Каталог',
        'header': 'Создай свой образ в  GeekShop!',
        'categories': ProductCategory.objects.all(),
    }
    context.update({
        'products': Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    })
    return render(request, 'products/products.html', context)
