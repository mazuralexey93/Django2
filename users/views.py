from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib import auth


from django.template.loader import render_to_string


from baskets.models import Basket
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from common.views import CommonContextMixin
from users.models import User


# class UserLoginView(CommonContextMixin, LoginView):
#     template_name = 'users/login.html'
#     form_class = UserLoginForm
#     title = 'GeekShop - Авторизация'

def login(request):
    title = 'входа'

    login_form = UserLoginForm(data=request.POST)
    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        passsword = request.POST['password']

        user = auth.authenticate(username=username, password=passsword)
        if user.activated:
            auth.authenticate()
            if user and user.is_active:
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if 'next' in request.POST.keys():
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect(reverse('index'))
        messages.error(request, 'Аккаунт не активирован')

    context = {
        'title': title,
        'login_form': login_form,
        'next': next,
    }

    return render(request, 'users/login.html', context)


class UserRegisterView(CommonContextMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    title = 'GeekShop - Регистрация'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались!'

    def register(request):
        title = 'регистрация'

        if request.method == 'POST':
            register_form = UserRegisterForm(request.POST, request.FILES)

            if register_form.is_valid():
                register_form.save()
                messages.success(request, "E-mail с подтверждением отправлен на Вашу элетронную почту")
                return HttpResponseRedirect(reverse('auth:login'))
        else:
            register_form = UserRegisterForm()

        context = {'title': title, 'register_form': register_form}

        return render(request, 'users/register.html', context)


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


def activate(request, pk):
    user = User.objects.filter(activation_key=pk).first()
    if not user:
        return redirect('/404')
    if not user.is_activation_key_expired():
        user.activated = True
        user.save()
        return render(request, 'users/success_activate.html')
    return render(request, 'users/activation_key_expired.html')