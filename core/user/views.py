from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserForm, UserProfileInfoForm

# Create your views here.


def index(request):
    return render(request, "user/index.html")


def register(request):
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        print(user_form)
        print(profile_form)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if "profile_img" in request.FILES:
                profile.profile_img = request.FILES["profile_img"]

            profile.save()
            registered = True
            context = {"registered": registered}
        else:
            print(user_form.errors, profile_form.errors)
    else:
        registered = False
        context = {
            "user_form": UserForm(),
            "profile_form": UserProfileInfoForm(),
            "registered": registered,
        }

    return render(request, "user/register.html", context)


def about_us(request):
    return render(request, "user/about_us.html")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def user_login(request):
    login_error = False
    is_active = True

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                is_active = False
        else:
            login_error = True
            print(f"{username} tried to login and failed")

    context = {"login_error": login_error, "is_active": is_active}
    return render(request, "user/login.html", context)
