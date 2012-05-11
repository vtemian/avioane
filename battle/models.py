from django.contrib.auth.models import User
from account.models import UserProfile
from django.db import models
from datetime import datetime

class Move(models.Model):
    x = models.CharField(max_length='30')
    y = models.CharField(max_length='30')
    owner = models.ForeignKey(UserProfile)

class Battle(models.Model):
    user = models.ForeignKey(User)
    enemy = models.ForeignKey(UserProfile)

    moves = models.ManyToManyField(Move, through='BattleMoves', null=True)

    finished = models.BooleanField(default=False)

class BattleMoves(models.Model):
    battle = models.ForeignKey(Battle)
    move = models.ForeignKey(Move)


class BattleInvitation(models.Model):
    fromUser = models.ForeignKey(User)
    toUser = models.ForeignKey(UserProfile)

    finished = models.BooleanField(default=False)

    start_time = models.DateTimeField(default=datetime.now())