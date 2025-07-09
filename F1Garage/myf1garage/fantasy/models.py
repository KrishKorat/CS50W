from django.contrib.auth.models import User
from django.db import models

class Constructor(models.Model):
    name = models.CharField(max_length=100)
    cost = models.FloatField()
    points = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Driver(models.Model):
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    cost = models.FloatField()
    points = models.FloatField(default=0)
    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Race(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class FantasyTeam(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Each user gets one team
    driver_1 = models.ForeignKey("Driver", on_delete=models.CASCADE, related_name="fantasy_teams_1")
    driver_2 = models.ForeignKey("Driver", on_delete=models.CASCADE, related_name="fantasy_teams_2")
    constructor = models.ForeignKey("Constructor", on_delete=models.CASCADE)
    total_cost = models.FloatField()
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Fantasy Team"
    

class RaceResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    position = models.IntegerField()
    points = models.IntegerField()

    def __str__(self):
        return f"{self.driver.name} - {self.race.name}"


class TeamScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    points = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.race.name}: {self.points} pts"


class SeasonScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    season_year = models.IntegerField()
    total_points = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "season_year")
        ordering = ["-total_points"]

    def __str__(self):
        return f"{self.user.username} - {self.season_year}: {self.total_points} pts"