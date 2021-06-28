from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from users.models import User
from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, AdminCategoryCreateForm, AdminCategoryUpdateForm
from products.models import ProductCategory
from common.views import CommonContextMixin


class UserIndexView(CommonContextMixin, TemplateView):
    title = 'Geekshop|Admin'
    template_name = 'admins/admin.html'


class UserListView(CommonContextMixin, ListView):
    model = User
    template_name = 'admins/admin_users_read.html'
    title = 'Geekshop|Admin - Пользователи'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


class UserCreateView(CommonContextMixin, CreateView):
    model = User
    title = 'Geekshop|Admin - Регистрация'
    template_name = 'admins/admin_users_create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admin_users')


class UserUpdateView(CommonContextMixin, UpdateView):
    model = User
    title = 'Geekshop|Admin - Обновление пользователя'
    template_name = 'admins/admin_users_update_delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')


class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin_users_update_delete.html'
    success_url = reverse_lazy('admins:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class UserUnDeleteView(UserDeleteView):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class AdminCategoriesListView(CommonContextMixin, ListView):
    model = ProductCategory
    title = 'Geekshop|Admin - Категории'
    template_name = 'admins/admin_categories.html'
    queryset = ProductCategory.objects.all()


class AdminCategoriesCreateView(CommonContextMixin, CreateView):
    model = ProductCategory
    title = 'Geekshop|Admin - Добавить категорию'
    template_name = 'admins/admin_categories_create.html'
    form_class = AdminCategoryCreateForm
    success_url = reverse_lazy('admins:admin_categories')


class AdminCategoriesUpdateView(CommonContextMixin, UpdateView):
    model = ProductCategory
    title = 'Geekshop|Admin -  Обновление категории'
    template_name = 'admins/admin_categories_update_delete.html'
    form_class = AdminCategoryUpdateForm
    success_url = reverse_lazy('admins:admin_categories')
    queryset = ProductCategory.objects.all()


class AdminCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'admins/admin_categories_update_delete.html'
    success_url = reverse_lazy('admins:admin_categories')
