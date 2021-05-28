from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

# Create your views here.
# функции = контроллер = представления = вьюшки/вьюхи


def index(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'products/index.html', context)


def products(request):
    return render(request, 'products/products.html')
