from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, "fantasy/index.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            messages.error(request, "Passwords must match.")
            return redirect("register")

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except:
            messages.error(request, "Username already taken.")
            return redirect("register")

        login(request, user)
        return redirect("index")
    
    return render(request, "fantasy/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid username and/or password.")
            return redirect("login")

    return render(request, "fantasy/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")
