from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from users.models import User
from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, AdminCategoryCreateForm, AdminCategoryUpdateForm
from products.models import ProductCategory


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'admins/admin.html')


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users(request):
#     context = {
#         'users': User.objects.all(),
#         'title': 'Geekshop|Admin - Пользователи'
#     }
#     return render(request, 'admins/admin_users_read.html', context)


class UserListView(ListView):
    model = User
    template_name = 'admins/admin_users_read.html'


class UserCreateView(CreateView):
    model = User
    template_name = 'admins/admin_users_create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admin_users')
#
#
# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             # messages.success(request, 'Пользователь успешно создан')
#             return HttpResponseRedirect(reverse('admins:admin_users'))
#     else:
#         form = UserAdminRegisterForm()
#     context = {
#         'title': 'Geekshop|Admin - Регистрация',
#         'form': form,
#     }
#     return render(request, 'admins/admin_users_create.html', context)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'admins/admin_users_update_delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')

#
# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_update(request, id):
#     selected_user = User.objects.get(id=id)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(data=request.POST, files=request.FILES, instance=selected_user)
#         if form.is_valid():
#             form.save()
#             # messages.success(request, 'Данные успешно обновлены!')
#             return HttpResponseRedirect(reverse('admins:admin_users'))
#     else:
#         form = UserAdminProfileForm(instance=selected_user)
#     context = {
#         'title': 'Geekshop|Admin - Обновление пользователя',
#         'form': form,
#         'selected_user': selected_user
#     }
#     return render(request, 'admins/admin_users_update_delete.html', context)


class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin_users_update_delete.html'
    success_url = reverse_lazy('admins:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
#
# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_delete(request, id):
#     user = User.objects.get(id=id)
#     user.is_active = False
#     user.save()
#     return HttpResponseRedirect(reverse('admins:admin_users'))


class UserUnDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin_users_update_delete.html'
    success_url = reverse_lazy('admins:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
# #
# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_undelete(request, id):
#     user = User.objects.get(id=id)
#     user.is_active = True
#     user.save()
#     return HttpResponseRedirect(reverse('admins:admin_users'))


def admin_categories(request):
    context = {
        'categories': ProductCategory.objects.all(),
        'title': 'Geekshop|Admin - Категории'
    }
    return render(request, 'admins/admin_categories.html', context)


def admin_categories_create(request):
    if request.method == 'POST':
        form = AdminCategoryCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_categories'))
    else:
        form = AdminCategoryCreateForm()
    context = {
        'form': AdminCategoryCreateForm(),
        'title': 'Geekshop|Admin - Добавить категории'
    }
    return render(request, 'admins/admin_categories_create.html', context)


def admin_categories_update(request, id):
    selected_category = ProductCategory.objects.get(id=id)
    if request.method == 'POST':
        form = AdminCategoryUpdateForm(data=request.POST, instance=selected_category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_categories'))
    else:
        form = AdminCategoryUpdateForm(instance=selected_category)
    context = {
        'title': 'Geekshop|Admin - Обновление категории',
        'form': form,
        'selected_category': selected_category
    }
    return render(request, 'admins/admin_categories_update_delete.html', context)


def admin_categories_delete(request, id):
    category = ProductCategory.objects.get(id=id)
    category.delete()
    return HttpResponseRedirect(reverse('admins:admin_categories'))
