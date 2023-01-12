from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from user.forms import UserRegisterForm

User = get_user_model()


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "user/user_register.html"
    success_url = reverse_lazy("user:user_login")


class UserLoginView(LoginView):
    template_name = "user/user_login.html"
    redirect_authenticated_user = True

    def get_default_redirect_url(self):
        return reverse("article:article_list")


class UserLogoutView(LogoutView):
    def get_default_redirect_url(self):
        return reverse("article:article_list")
