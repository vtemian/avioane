from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from medals.models import Medal
import json
import urllib

class Alliance(models.Model):
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(User, null=True, through="alliance.AllianceMembership")
    radar=models.IntegerField(default=0)
    lvl = models.IntegerField(default=1)
    respect = models.IntegerField(default=1)
    medals=models.ManyToManyField(Medal, null=True, through="alliance.AllianceMedals")

    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d', null=True)

class AllianceMembership(models.Model):
    alliance = models.ForeignKey(Alliance)
    profile = models.ForeignKey(User)

    rank = models.CharField(max_length=30)

class AllianceMedals(models.Model):
    medal = models.ForeignKey(Medal)
    alliance = models.ForeignKey(Alliance)

class Vote(models.Model):
    profile = models.ForeignKey(User)

    created_at = models.DateField(default=datetime.now())

    class Meta:
        abstract = True

class Like(Vote):
    type = models.CharField(max_length=30, default="like")

class Unlike(Vote):
    type = models.CharField(max_length=30, default="unlike")

class AllianceNews(models.Model):
    alliance = models.ForeignKey(Alliance)
    profile = models.ForeignKey(User)

    title = models.CharField(max_length=50)
    created_at = models.DateField(default=datetime.now())
    text = models.TextField(null=True)
    type = models.CharField(max_length=30, default="simple")

    like = models.ManyToManyField(Like)
    unlike = models.ManyToManyField(Unlike)