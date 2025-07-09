from django.core.management.base import BaseCommand
from django.db.models import Sum
from fantasy.models import FantasyTeam, RaceResult

class Command(BaseCommand):
    help = "Assign season total points to all fantasy teams"

    def handle(self, *args, **options):
        for team in FantasyTeam.objects.all():
            driver_ids = [team.driver_1.id, team.driver_2.id]

            # Total points scored by driver's results
            driver_points = RaceResult.objects.filter(driver__id__in=driver_ids).aggregate(total=Sum("points"))["total"] or 0

            # Points scored by all drivers belonging to the same constructor
            constructor_driver_ids = team.constructor.driver_set.values_list("id", flat=True)
            constructor_points = RaceResult.objects.filter(driver__id__in=constructor_driver_ids).aggregate(total=Sum("points"))["total"] or 0

            total_points = driver_points + constructor_points
            team.points = total_points
            team.save()

            self.stdout.write(f"{team.user.username}: {total_points} points assigned")
