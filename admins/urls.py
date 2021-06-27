from django.urls import path

from admins.views import UserIndexView, UserListView, UserDeleteView, UserUpdateView, UserCreateView,\
    UserUnDeleteView, AdminCategoriesListView, AdminCategoriesCreateView, AdminCategoriesUpdateView, AdminCategoryDeleteView

app_name = 'admins'

urlpatterns = [
    path('', UserIndexView.as_view(), name='index'),

    path('users/', UserListView.as_view(), name='admin_users'),
    path('users/create', UserCreateView.as_view(), name='admin_users_create'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='admin_users_delete'),
    path('users/undelete/<int:pk>/', UserUnDeleteView.as_view(), name='admin_users_undelete'),

    path('categories/', AdminCategoriesListView.as_view(), name='admin_categories'),
    path('categories/create', AdminCategoriesCreateView.as_view(), name='admin_categories_create'),
    path('categories/update/<int:pk>/', AdminCategoriesUpdateView.as_view(), name='admin_categories_update'),
    path('categories/delete/<int:pk>/', AdminCategoryDeleteView.as_view(), name='admin_categories_delete'),

]
