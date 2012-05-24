from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from division.models import Division
import json
import urllib
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    gravatar_url = models.CharField(max_length=100)
    facebook_id = models.BigIntegerField(null=True)
    access_token = models.CharField(max_length=150)

    def get_facebook_profile(self):
        fb_profile = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % self.access_token)
        return json.load(fb_profile)

class UserStats(models.Model):
    user = models.ForeignKey(UserProfile)

    money = models.IntegerField(null=True, default=10)
    exp = models.IntegerField(null=True, default=0)
    lvl = models.IntegerField(default=1)
    rank = models.CharField(max_length=30, default='Second Lieutenant')
    achieve_points = models.IntegerField(default=0)

    won = models.IntegerField(null=True, default=0)
    lost = models.IntegerField(null=True, default=0)

class UserDivision(models.Model):
    user = models.ForeignKey(UserStats)
    name = models.CharField(max_length=30, default='D')

    points = models.IntegerField(max_length=30, default=0)

    matches_played = models.IntegerField(max_length=30, default=0)

class PasswordReset(models.Model):
    email = models.EmailField(max_length=50)
    token = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=datetime.now)
    done = models.BooleanField(default=False)