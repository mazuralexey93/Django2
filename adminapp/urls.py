from django.urls import path
import adminapp.views as adminapp
app_name = 'adminapp'

urlpatterns = [
    path('authapp/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('authapp/read/', adminapp.UserListView.as_view(), name='authapp'),
    path('authapp/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('authapp/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),

    path('categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/read/', adminapp.categories, name='categories'),
    path('categories/update/<int:pk>/', adminapp.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.CategoryDeleteView.as_view(), name='category_delete'),

    path('products/create/category/<int:pk>/', adminapp.product_create, name='product_create'),
    path('products/read/category/<int:pk>/', adminapp.ProductsListView.as_view(), name='products'),
    path('products/read/<int:pk>/', adminapp.product_read, name='product_read'),
    path('products/update/<int:pk>/', adminapp.product_update, name='product_update'),
    path('products/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),
]
