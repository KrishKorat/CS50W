from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Driver(models.Model):
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    cost = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.team})"

class Constructor(models.Model):
    name = models.CharField(max_length=100)
    cost = models.IntegerField()

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
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver_1 = models.ForeignKey(Driver, related_name='driver1', on_delete=models.CASCADE)
    driver_2 = models.ForeignKey(Driver, related_name='driver2', on_delete=models.CASCADE)
    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)
    total_cost = models.IntegerField()
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s team for {self.race}"

class RaceResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    position = models.IntegerField()
    fastest_lap = models.BooleanField(default=False)

    def __str__(self):
      return f"{self.driver.name} - {self.race.name} - P{self.position}"
