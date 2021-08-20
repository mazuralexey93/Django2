from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product
from ordersapp.models import Order


def get_data(user):
    return Order.objects.select_related('user').all()


def index(request):

    data = get_data(request.user)
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
        'data': data
    }
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    return render(request, 'geekshop/contact.html')
