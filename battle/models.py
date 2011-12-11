from django.contrib.auth.models import User
from account.models import UserProfile
from django.db import models

class Battle(models.Model):
    user = models.ForeignKey(User)
    enemy = models.ForeignKey(UserProfile)