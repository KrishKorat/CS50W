from .models import RaceResult, FantasyTeam

POINTS_TABLE = {
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

def calculate_fantasy_points(race):
    results = RaceResult.objects.filter(race=race)
    fastest_lap_driver_ids = results.filter(fastest_lap=True).values_list('driver_id', flat=True)

    teams = FantasyTeam.objects.filter(race=race)

    for team in teams:
        score = 0
        for driver in [team.driver_1, team.driver_2]:
            try:
                result = results.get(driver=driver)
                position_points = POINTS_TABLE.get(result.position, 0)
                score += position_points
                if result.driver.id in fastest_lap_driver_ids:
                    score += 1
            except RaceResult.DoesNotExist:
                pass

        team.points = score
        team.save()
