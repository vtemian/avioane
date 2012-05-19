__author__ = 'Al'
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import json
import urllib

class division(models.Model):
    name=models.IntegerField(default= 1)
    pointsUp= models.IntegerField()
    pointsDown= models.IntegerField()
    dateAdded= models.DateTimeField(default=datetime.now())
    League= models.ManyToManyField(Leagues, through='DivisionLeagues', null=true)

class Leagues(models.Model):
    name= models.CharField(max_length=2, default='D')
    dateAdded= models.DateTimeField(default=datetime.now())

class DivisionLeagues(models.Model):
    division=models.ForeignKey(division)
    league=models.ForeignKey(Leagues)
