from django.core.management.base import BaseCommand
from fantasy.models import FantasyTeam, SeasonScore

SEASON_YEAR = 2025

class Command(BaseCommand):
    help = "Update SeasonScore based on FantasyTeam points"

    def handle(self, *args, **kwargs):
        for team in FantasyTeam.objects.all():
            score_obj, created = SeasonScore.objects.get_or_create(
                user=team.user,
                season_year=SEASON_YEAR
            )
            score_obj.total_points = team.points or 0
            score_obj.save()

            msg = f"{'Created' if created else 'Updated'} score for {team.user.username}: {score_obj.total_points} pts"
            self.stdout.write(self.style.SUCCESS(msg))
