from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import json
import urllib

class Weapons(models.Model):
    name = models.CharField(max_length=2, default='a')
    image = models.CharField(max_length=50, dafault='ImagePath')

    description = models.TextField(null=True)

class Division(models.Model):
    name = models.CharField(max_length=2, default='D')
    go_up_points = models.IntegerField(max_length=5)
    go_down_points = models.IntegerField(max_length=5)

    plane_type = models.CharField(default="airborne", max_length=10)

    achieve_points = models.IntegerField(max_length=500, default='10')

    weapons = models.ManyToManyField(Weapons, through='DivisionWeapons', null=True)

class DivisionWeapons(models.Model):
    division = models.ForeignKey(Division)
    weapons = models.ForeignKey(Weapons)