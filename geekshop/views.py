from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product
from ordersapp.models import Order
from django.views.decorators.cache import cache_page, never_cache


def get_data(user):
    return Order.objects.select_related('user').all()


@never_cache
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


# Кэширование вьюшки декоратором
@cache_page(300)
def contacts(request):
    return render(request, 'geekshop/contact.html')


from django.core.cache import cache
from django.conf import settings


# Пример использования низкоуровневого кэширования
def _get_active_products():
    return Product.objects.select_related().all()


def get_product(request):
    if settings.LOW_CACHE:
        cached_products = cache.get('products')
        if cached_products is None:
            cache.set('products', _get_active_products())
        return cached_products
    else:
        return _get_active_products()


