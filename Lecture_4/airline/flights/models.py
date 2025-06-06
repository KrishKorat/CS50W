from django.db import models

# Create your models here.

class Airport(models.Model):
  code = models.CharField(max_length=3)
  city = models.CharField(max_length=64)

  def __str__(self):
    return f"{self.city} ({self.code})" 

class Flight(models.Model):
  origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
  destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
  duration = models.IntegerField()

  def __str__(self):
    return f"{self.id}: {self.origin} to {self.destination}"



class Passenger(models.Model):
  first = models.CharField(max_length=64)
  last = models.CharField(max_length=64)
  flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

  def __str__(self):
    return f"{self.first} {self.last}"


'''
>>> from flights.models import Flight
>>> f = Flight(origin="New York", destination="London", duration=415)
>>> f.save()
>>> Flight.objects.all()
<QuerySet [<Flight: Flight object (1)>]>


-------------------------------------------- After defining __str__

>>> from flights.models import Flight
>>> flights = Flight.objects.all()
>>> flights
<QuerySet [<Flight: 1: New York to London>]>

>>> flight = flights.first()
>>> flight 
<Flight: 1: New York to London>
>>> flight.id
1
>>> flight.origin 
'New York'
>>> flight.destination
'London'
'''




'''
-------------------------------------------------- After changing to foreign keys

>>> from flights.models import Airport

>>> jfk = Airport(code="JFK", city="New York")
>>> jfk.save()

>>> lhr = Airport(code="LHR", city="London")
>>> lhr.save()

>>> cdg = Airport(code="CDG", city="Paris")
>>> cdg.save()

>>> nrt = Airport(code="NRT", city="Tokyo")
>>> nrt.save()

>>> f = Flight(origin=jfk, destination=lhr, duration=415)
>>> f.save()
>>> f
<Flight: 1: New York (JFK) to London (LHR)>

>>> f.origin  
<Airport: New York (JFK)>
>>> f.origin.city
'New York'
>>> f.origin.code
'JFK'

>>> lhr.arrivals.all()
<QuerySet [<Flight: 1: New York (JFK) to London (LHR)>]>
'''


'''
>>> Airport.objects.all()
<QuerySet [<Airport: New York (JFK)>, <Airport: London (LHR)>, <Airport: Paris (CDG)>, <Airport: Tokyo (NRT)>]>

>>> Airport.objects.filter(city="New York")
<QuerySet [<Airport: New York (JFK)>]>

>>> Airport.objects.filter(city="New York").first()
<Airport: New York (JFK)>

>>> Airport.objects.get(city="New York")        
<Airport: New York (JFK)>
'''

'''
----------------------------------------------------------------------- Adding 2nd flight
>>> jfk = Airport.objects.get(city="New York")
>>> cdg = Airport.objects.get(city="Paris")
>>> cdg
<Airport: Paris (CDG)>
>>> f = Flight(origin=jfk, destination=cdg, duration=435)
>>> f.save()
'''