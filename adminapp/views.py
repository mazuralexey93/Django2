from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from adminapp.forms import UserRegisterForm, ProductEditForm, ProductCategoryEditForm
from authapp.models import User
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test

from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'adminapp/admin_users.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return User.objects.filter(is_delete=False)


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'adminapp/admin_users_form.html'
    success_url = reverse_lazy('admin_staff:authapp')


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        edit_form = UserRegisterForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()

            return HttpResponseRedirect(reverse('admin_staff:user_update', args=[edit_user.pk]))
    else:
        edit_form = UserRegisterForm(instance=edit_user)

    context = {
        'title': title,
        'update_form': edit_form,
    }

    return render(request, 'adminapp/admin_users_update.html', context)


def user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user.is_delete = True
        user.is_active = False
        user.save()

        return HttpResponseRedirect(reverse('admin_staff:authapp'))

    context = {
        'title': title,
        'user_to_delete': user,
    }

    return render(request, 'adminapp/admin_users_delete.html', context)


def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    content = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/admin_categories.html', content)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/admin_category_create.html'
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context


def category_update(request, pk):
    title = 'категория/редактирование'

    edit_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:category_update', args=[edit_category.pk]))
    else:
        edit_form = ProductCategoryEditForm(instance=edit_category)

    context = {'title': title,
               'form': edit_form,
               }

    return render(request, 'adminapp/admin_category_create.html', context)


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/admin_category_delete.html'
    context_object_name = 'category_to_delete'
    success_url = reverse_lazy('admin_staff:categories')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/admin_category_create.html'
    success_url = reverse_lazy('admin_staff:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))

        return super().form_valid(form)


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/admin_products.html'

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)

        category = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))

        context.update({'category': category})

        return context


def products(request, pk):
    title = 'админка/категории продуктов'

    if pk == 0:
        categories = ProductCategory.objects.filter(is_delete=False)
        context = {
            'title': title,
            'objects': categories,
        }

        return render(request, 'adminapp/admin_categories.html', context)

    category = get_object_or_404(ProductCategory, pk=pk)
    products_category = Product.objects.filter(category__pk=pk)

    content = {
        'title': title,
        'category': category,
        'objects': products_category,
    }

    return render(request, 'adminapp/admin_products.html', content)


def product_create(request, pk):
    title = 'продукты/создание'
    product_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()

            return HttpResponseRedirect(reverse('admin_staff:products'), args=[pk])
    else:
        product_form = ProductEditForm(initial={'category': product_category})

    context = {
        'title': title,
        'update_form': product_form,
        'category': product_category
    }

    return render(request, 'adminapp/admin_product_update.html', context)


def product_read(request, pk):
    product = get_object_or_404(Product, pk=pk)
    title = f'продукты/{product.name}'

    context = {
        'title': title,
        'product': product,
    }

    return render(request, 'adminapp/admin_product_read.html', context)


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    title = f'продукты/{product.name}'

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()

            return HttpResponseRedirect(reverse('admin_staff:product_update', args=[product_form.pk]))
    else:
        product_form = ProductEditForm(instance=product)

    context = {
        'title': title,
        'form': product_form,
        'category': product.category
    }

    return render(request, 'adminapp/admin_product_update.html', context)


def product_delete(request, pk):
    title = 'пользователи/удаление'

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_delete = True
        product.save()

        return HttpResponseRedirect(reverse('admin_staff:products', args=[product.category.pk]))

    context = {
        'title': title,
        'product_to_delete': product,
    }

    return render(request, 'adminapp/admin_product_delete.html', context)
