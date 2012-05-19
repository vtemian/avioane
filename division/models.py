from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import json
import urllib

class Leagues(models.Model):
    name= models.CharField(max_length=2, default='D')
    dateAdded= models.DateTimeField(default=datetime.now())



class divisions(models.Model):
    name=models.IntegerField(default= 1)
    pointsUp= models.IntegerField()
    pointsDown= models.IntegerField()
    dateAdded= models.DateTimeField(default=datetime.now())
    League= models.ManyToManyField(Leagues, through='DivisionsLeagues')


class DivisionsLeagues(models.Model):
    divisions=models.ForeignKey(divisions)
    leagues=models.ForeignKey(Leagues)