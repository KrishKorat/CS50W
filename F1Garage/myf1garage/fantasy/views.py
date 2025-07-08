from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Driver, Constructor, FantasyTeam, Race
from django.http import Http404

from django.db.models import F, Sum, Value
from django.db.models.functions import Coalesce

# Create your views here.

def index(request):
    return render(request, "fantasy/index.html")


@login_required
def create_fantasy_team(request):
    drivers = Driver.objects.all().order_by('-cost')
    constructors = Constructor.objects.all().order_by('-cost')
    races = Race.objects.all()
    MAX_BUDGET = 100

    if request.method == "POST":
        d1_id = request.POST.get("driver_1")
        d2_id = request.POST.get("driver_2")
        constructor_id = request.POST.get("constructor")
        race_id = request.POST.get("race")

        if d1_id == d2_id:
            messages.error(request, "Please select two different drivers.")
        else:
            d1 = Driver.objects.get(id=d1_id)
            d2 = Driver.objects.get(id=d2_id)
            constructor = Constructor.objects.get(id=constructor_id)
            race = Race.objects.get(id=race_id)

            total_cost = d1.cost + d2.cost + constructor.cost

            if total_cost > MAX_BUDGET:
                messages.error(request, f"Budget exceeded! Total: ${total_cost}M (Max: ${MAX_BUDGET}M)")
            else:
                team, created = FantasyTeam.objects.get_or_create(
                    user=request.user,
                    race=race,
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

                messages.success(request, f"Fantasy team saved for {race.name}!")
                return redirect("view_team", race_id=race.id)

    return render(request, "fantasy/create_team.html", {
        "drivers": drivers,
        "constructors": constructors,
        "races": races,
        "budget": MAX_BUDGET,
    })




@login_required
def view_fantasy_team(request, race_id):
    races = Race.objects.all()
    race = get_object_or_404(Race, id=race_id)

    team = FantasyTeam.objects.filter(user=request.user, race=race).first()

    return render(request, "fantasy/view_team.html", {
        "selected_race": race,
        "races": races,
        "team": team,
    })




@login_required
def view_fantasy_team_redirect(request):
    # Redirect to first available race the user has a team for
    team = FantasyTeam.objects.filter(user=request.user).order_by('-race__date').first()
    if team:
        return redirect("view_team", race_id=team.race.id)
    else:
        messages.info(request, "Please create a fantasy team first.")
        return redirect("create_team")









@login_required
def leaderboard(request):
    print("🏁 Rendering leaderboard")

    leaderboard_data = (
        FantasyTeam.objects
        .values(
            "user__username",
            "driver_1__name",
            "driver_2__name",
            "constructor__name",
            "race__name",
            "total_cost"
        )
        .annotate(
            total_points=Sum(
                F("driver_1__points") + F("driver_2__points") + F("constructor__points")
            )
        )
        .order_by("-total_points")
    )

    return render(request, "fantasy/leaderboard.html", {
        "leaderboard": leaderboard_data
    })













@login_required
def assign_points(request):
    if not request.user.is_superuser:
        return redirect("index")  # deny access to non-admins

    race = Race.objects.first()  # later support selecting race
    calculate_fantasy_points(race)
    messages.success(request, f"Points calculated and updated for {race.name}!")
    return redirect("admin:index")


def calculate_fantasy_points(race):
    """
    Dummy implementation: Assigns random or zero points to all fantasy teams for the given race.
    Replace this logic with your actual points calculation.
    """
    if not race:
        return
    teams = FantasyTeam.objects.filter(race=race)
    for team in teams:
        # Example: set points to 0 (replace with real calculation)
        team.points = 0
        team.save()















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
