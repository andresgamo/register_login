from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("register", views.register, name="register"),
    path("about_us", views.about_us, name="about_us"),
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
]
