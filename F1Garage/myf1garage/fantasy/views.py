from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Driver, Constructor, FantasyTeam, Race, SeasonScore, RaceResult
from django.http import Http404

from django.db.models import F, Sum, Value
from django.db.models.functions import Coalesce
from datetime import date

from .utils import recalculate_all_points


# Create your views here.

def index(request):
    constructors = Constructor.objects.all()
    races = Race.objects.all()
    
    upcoming_race = Race.objects.filter(date__gte=date.today()).order_by('date').first()

    leaderboard = (
        SeasonScore.objects
        .filter(season_year=2025)
        .select_related('user')
        .order_by('-total_points')[:5]
    )

    return render(request, "fantasy/index.html", {
        "constructors": constructors,
        "races": races,
        "upcoming_race": upcoming_race,
        "leaderboard": leaderboard,
    })



@login_required
def create_fantasy_team(request):
    user = request.user

    existing_team = FantasyTeam.objects.filter(user=user).first()
    if existing_team:
        return redirect("view_team", team_id=existing_team.id)

    drivers = Driver.objects.all()
    constructors = Constructor.objects.all()

    if request.method == "POST":
        driver_1_id = request.POST.get("driver_1")
        driver_2_id = request.POST.get("driver_2")
        constructor_id = request.POST.get("constructor")

        driver_1 = get_object_or_404(Driver, id=driver_1_id)
        driver_2 = get_object_or_404(Driver, id=driver_2_id)
        constructor = get_object_or_404(Constructor, id=constructor_id)

        total_cost = driver_1.cost + driver_2.cost + constructor.cost

        if total_cost > 100:
            return render(request, "fantasy/create_team.html", {
                "drivers": drivers,
                "constructors": constructors,
                "error": "Budget exceeded! Choose cheaper team members.",
                "remaining_budget": 100 - total_cost
            })

        # Save the team
        FantasyTeam.objects.create(
            user=user,
            driver_1=driver_1,
            driver_2=driver_2,
            constructor=constructor,
            total_cost=total_cost
        )

        # ✅ Recalculate points for everyone
        recalculate_all_points()

        return redirect("view_team", team_id=user.fantasyteam.id)

    return render(request, "fantasy/create_team.html", {
        "drivers": drivers,
        "constructors": constructors,
        "remaining_budget": 100
    })




@login_required
def edit_fantasy_team(request):
    user = request.user
    team = get_object_or_404(FantasyTeam, user=user)

    drivers = Driver.objects.all().order_by('-cost')
    constructors = Constructor.objects.all().order_by('-cost')

    if request.method == "POST":
        driver_1_id = request.POST.get("driver_1")
        driver_2_id = request.POST.get("driver_2")
        constructor_id = request.POST.get("constructor")

        driver_1 = get_object_or_404(Driver, id=driver_1_id)
        driver_2 = get_object_or_404(Driver, id=driver_2_id)
        constructor = get_object_or_404(Constructor, id=constructor_id)

        total_cost = driver_1.cost + driver_2.cost + constructor.cost

        if total_cost > 100:
            return render(request, "fantasy/edit_team.html", {
                "drivers": drivers,
                "constructors": constructors,
                "team": team,
                "error": "Budget exceeded! Choose cheaper team members.",
                "remaining_budget": 100 - total_cost
            })

        # ✅ Update team
        team.driver_1 = driver_1
        team.driver_2 = driver_2
        team.constructor = constructor
        team.total_cost = total_cost
        team.save()

        # ✅ Recalculate points immediately
        recalculate_all_points()

        return redirect("view_team_redirect")

    return render(request, "fantasy/edit_team.html", {
        "drivers": drivers,
        "constructors": constructors,
        "team": team,
        "remaining_budget": 100 - team.total_cost
    })







from django.shortcuts import get_object_or_404

@login_required
def view_fantasy_team(request, team_id):
    team = get_object_or_404(FantasyTeam, id=team_id, user=request.user)

    return render(request, "fantasy/view_team.html", {
        "team": team
    })




@login_required
def view_fantasy_team_redirect(request):
    try:
        team = FantasyTeam.objects.get(user=request.user)
    except FantasyTeam.DoesNotExist:
        return redirect("create_team")

    return render(request, "fantasy/view_team.html", {
        "team": team
    })









def leaderboard(request):
    leaderboard_data = (
        SeasonScore.objects
        .select_related("user")
        .order_by("-total_points")
    )
    return render(request, "fantasy/leaderboard.html", {
        "leaderboard": leaderboard_data
    })












from .utils import recalculate_all_points

@login_required
@user_passes_test(lambda u: u.is_superuser)
def assign_points(request):
    recalculate_all_points()
    return render(request, "fantasy/assign_points_success.html")





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
