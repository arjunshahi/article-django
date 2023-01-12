from django.urls import path

from user import views as user_views

app_name = "user"

urlpatterns = [
    path("register/", user_views.UserRegisterView.as_view(), name="user_register"),
    path("login/", user_views.UserLoginView.as_view(), name="user_login"),
    path("logout/", user_views.UserLogoutView.as_view(), name="user_logout"),

]
