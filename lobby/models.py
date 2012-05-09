from account.models import UserProfile
from django.db import models

class WaitingUser(models.Model):
    user = models.ForeignKey(UserProfile)
