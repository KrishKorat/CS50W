from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follow
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator


@login_required
def index(request):
    all_posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(all_posts, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj
    })


@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST.get("content")
        if content.strip():
            Post.objects.create(author=request.user, content=content)

    return HttpResponseRedirect(reverse("index"))



@login_required
def profile(request, username):

    profile_user = get_object_or_404(User, username=username)
    all_posts = Post.objects.filter(author=profile_user).order_by("-timestamp")

    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()


    is_following = False
    if request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    
    if request.method == "POST":
        if is_following:
            Follow.objects.filter(follower=request.user, following=profile_user).delete()
        else:
            Follow.objects.create(followe=request.user, following=profile_user)
        return redirect("profile", username=username)


    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "page_obj": page_obj,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following
    })



@login_required
def following(request):

    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)

    all_posts = Post.objects.filter(author__id__in=following_users).order_by('-timestamp')

    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })






def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
