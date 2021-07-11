from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product


def index(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    title = 'geekshop'
    products = Product.objects.all()[:4]

    context = {
        'mainapp': products,
        'some_name': 'hello',
        'title': title,
        'basket': basket,
    }
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    return render(request, 'geekshop/contact.html')
