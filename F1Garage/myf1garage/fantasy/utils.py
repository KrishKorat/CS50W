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
