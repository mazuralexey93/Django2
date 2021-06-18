from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from users.models import User
from admins.forms import UserAdminRegisterForm, UserAdminProfileForm


def index(request):
    return render(request, 'admins/admin.html')


def admin_users(request):
    context = {
        'users': User.objects.all(),
        'title': 'Geekshop|Admin - Пользователи'
    }
    return render(request, 'admins/admin_users_read.html', context)


def admin_users_create(request):
    if request.method == 'POST':
        form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Пользователь успешно создан')
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminRegisterForm()
    context = {
        'title': 'Geekshop|Admin - Регистрация',
        'form': form,
    }
    return render(request, 'admins/admin_users_create.html', context)


def admin_users_update(request, id):
    selected_user = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserAdminProfileForm(data=request.POST, files=request.FILES, instance=selected_user)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Данные успешно обновлены!')
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminProfileForm(instance=selected_user)
    context = {
        'title': 'Geekshop|Admin - Обновление пользователя',
        'form': form,
        'selected_user': selected_user
    }
    return render(request, 'admins/admin_users_update_delete.html', context)


def admin_users_delete(request, id):
    pass
