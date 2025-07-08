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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver_1 = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='fantasy_driver1')
    driver_2 = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='fantasy_driver2')
    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    total_cost = models.FloatField()

    def __str__(self):
        return f"{self.user.username}'s Team for {self.race.name}"


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
