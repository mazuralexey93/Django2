from django.shortcuts import render

from users.models import User


def index(request):
    return render(request, 'admins/admin.html')


def admin_users(request):
    context = {'users': User.objects.all()}
    return render(request, 'admins/admin_users_read.html', context)


def admin_users_create(request):
    return render(request, 'admins/admin_users_create.html')


def admin_users_update(request, id):
    return render(request, 'admins/admin_users_update_delete.html')


def admin_users_delete(request, id):
    pass
