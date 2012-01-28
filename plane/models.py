from django.db import models
from account.models import UserProfile
from battle.models import Battle

class Coordinates(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

class Plane(models.Model):
    position = models.ManyToManyRel(Coordinates, through="Positioning")
    owner = models.ForeignKey(UserProfile)
    battle = models.ForeignKey(Battle)
    type = models.CharField(default='plane1', max_length=10)
    dead = models.BooleanField(default=False)

class Positioning(models.Model):
    plane = models.ForeignKey(Plane)
    coordinates = models.ForeignKey(Coordinates)