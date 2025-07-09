from django.contrib import admin
from .models import Driver, Constructor, Race, FantasyTeam, RaceResult, SeasonScore

# Register your models here.

admin.site.register(Driver)
admin.site.register(Constructor)
admin.site.register(Race)
admin.site.register(FantasyTeam)
admin.site.register(RaceResult)
admin.site.register(SeasonScore)
