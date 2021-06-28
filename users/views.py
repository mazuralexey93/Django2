from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from baskets.models import Basket
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from common.views import CommonContextMixin
from users.models import User


class UserLoginView(CommonContextMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'GeekShop - Авторизация'


class UserRegisterView(CommonContextMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    title = 'GeekShop - Регистрация'
    success_url = 'users:login'
    success_message = 'Вы успешно зарегистрировались!'


class UserProfileView(CommonContextMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    title = 'Geekshop - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context


class UserLogoutView(LogoutView):
    pass
