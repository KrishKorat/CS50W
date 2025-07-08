from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Driver, Constructor, FantasyTeam, Race
from django.http import Http404


# Create your views here.

def index(request):
    return render(request, "fantasy/index.html")


@login_required
def create_fantasy_team(request):
    drivers = Driver.objects.all()
    constructors = Constructor.objects.all()
    race = Race.objects.first()  # later allow user to pick race
    MAX_BUDGET = 50

    if request.method == "POST":
        d1_id = request.POST.get("driver_1")
        d2_id = request.POST.get("driver_2")
        constructor_id = request.POST.get("constructor")

        if d1_id == d2_id:
            messages.error(request, "Please select two different drivers.")
        else:
            d1 = Driver.objects.get(id=d1_id)
            d2 = Driver.objects.get(id=d2_id)
            constructor = Constructor.objects.get(id=constructor_id)

            total_cost = d1.cost + d2.cost + constructor.cost

            if total_cost > MAX_BUDGET:
                messages.error(request, f"Budget exceeded! Total: ${total_cost}M (Max: ${MAX_BUDGET}M)")
            else:
                # Check if team already exists for this user and race
                team, created = FantasyTeam.objects.get_or_create(
                    user=request.user, race=race,
                    defaults={
                        "driver_1": d1,
                        "driver_2": d2,
                        "constructor": constructor,
                        "total_cost": total_cost,
                    }
                )
                if not created:
                    team.driver_1 = d1
                    team.driver_2 = d2
                    team.constructor = constructor
                    team.total_cost = total_cost
                    team.save()

                messages.success(request, "Fantasy team saved successfully!")
                return redirect("view_team")

    return render(request, "fantasy/create_team.html", {
        "drivers": drivers,
        "constructors": constructors,
        "budget": MAX_BUDGET,
    })


@login_required
def view_fantasy_team(request):
    race = Race.objects.first()  # Replace with selected race later
    try:
        team = FantasyTeam.objects.get(user=request.user, race=race)
    except FantasyTeam.DoesNotExist:
        team = None

    return render(request, "fantasy/view_team.html", {
        "team": team,
        "race": race
    })



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
