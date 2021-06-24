from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, UserDetailsForm
from .models import User
from django.contrib.auth import logout
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return render(request, "auth.html")
    return render(request, "unauth.html")


def RegisterView(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "signup.html", {"form": form})
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account successfully created")
            return redirect("login")
        else:
            messages.error(request, "Invalid data")
            return redirect("register")


def Logout(request):

    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("/")


def LoginView(request):
    if request.method == "GET":
        f = LoginForm()
        return render(request, "login.html", {"form": f})
    elif request.method == "POST":
        f = LoginForm(request.POST)
        if f.is_valid():

            user = auth.authenticate(
                email=request.POST.get("email"), password=request.POST.get("password")
            )
            if user is not None:  # valid user
                auth.login(request, user)
                messages.success(request, "You have been Loged in")
                return redirect("/")

        messages.info(request, "invalid username or password")
        return redirect("login")


@login_required(login_url="/login/")
def account_details(request):
    if request.method == "GET":
        f = UserDetailsForm()
        return render(request, "account.html", {"form": f, "user": request.user})
    method = request.POST.get("_method", "").lower()
    if request.method == "POST":
        # create an object and redirect to detail page
        form = UserDetailsForm(request.POST or None, instance=request.user)
        if (
            request.user.email != request.POST.get("email")
            and request.POST.get("email") is not None
        ):
            print(request.user.email)
            print(request.POST.get("email"))
            messages.error(request, "You are not allowed to change your email")
            return redirect("account-details")
        user = User.objects.filter(email=request.user.email)[0]
        username = request.POST["username"]
        address = request.POST["address"]
        if (
            User.objects.filter(username=username).exists()
            and user.username != username
            and username is None
        ):
            messages.error(request, "username already in use, please try another")
            return redirect("account-details")
        if username is not None:
            user.username = username
        if address is not None:
            user.address = address
        user.save()
        messages.success(request, "Your details have been updated")
        return redirect("account-details")

    if method == "delete":
        email = request.user.email
        user = User.objects.filter(email=email).delete()
        messages.info(request, " data deleted ")
        return redirect("register")
    return redirect("account-details")
