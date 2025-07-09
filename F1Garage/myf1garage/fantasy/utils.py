from .models import RaceResult

def calculate_team_points(team):
    points = 0
    race = team.race

    # Points logic — mock or actual F1 style
    scoring = {
        1: 25,
        2: 18,
        3: 15,
        4: 12,
        5: 10,
        6: 8,
        7: 6,
        8: 4,
        9: 2,
        10: 1
    }

    for driver in [team.driver_1, team.driver_2]:
        try:
            result = RaceResult.objects.get(driver=driver, race=race)
            points += scoring.get(result.position, 0)
            if result.fastest_lap:
                points += 1
        except RaceResult.DoesNotExist:
            continue

    # Simple constructor bonus
    if team.constructor.name.lower() in [team.driver_1.team.lower(), team.driver_2.team.lower()]:
        points += 10  # or adjust logic

    team.points = points
    team.save()
    return points




from .models import Driver, Constructor, RaceResult, FantasyTeam, SeasonScore
from django.db.models import Sum

def recalculate_all_points():
    # 1. Reset all driver and constructor points
    Driver.objects.update(points=0)
    Constructor.objects.update(points=0)

    # 2. Assign driver points from RaceResult
    for result in RaceResult.objects.all():
        driver = result.driver
        driver.points += result.points
        driver.save()

    # 3. Assign constructor points (sum of all its drivers' points)
    for constructor in Constructor.objects.all():
        total_driver_points = Driver.objects.filter(constructor=constructor).aggregate(
            total=Sum('points')
        )['total'] or 0
        constructor.points = total_driver_points
        constructor.save()

    # 4. Update FantasyTeam points
    teams = FantasyTeam.objects.select_related("driver_1", "driver_2", "constructor")
    for team in teams:
        team.points = (
            team.driver_1.points +
            team.driver_2.points +
            team.constructor.points
        )
        team.save()

    # 5. Update SeasonScore
    for team in teams:
        score_obj, _ = SeasonScore.objects.get_or_create(
            user=team.user,
            season_year=2025
        )
        score_obj.total_points = team.points
        score_obj.save()
