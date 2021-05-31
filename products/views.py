from django.shortcuts import render
# Create your views here.

from django.shortcuts import render

import json
import os

MODULE_DIR = os.path.dirname(__file__)


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
        'header': 'Создай свой образ в  GeekShop!'
    }
    file_path = os.path.join(MODULE_DIR, 'fixtures/products.json')
    context['products'] = json.load(open(file_path, encoding='utf-8'))

    return render(request, 'products/products.html', context)
