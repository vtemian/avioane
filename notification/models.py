from datetime import datetime
from django.db import models
from account.models import UserProfile
#from profile.models import Friend

class Notification(models.Model):
    created_at = models.DateTimeField(default=datetime.now())
    message = models.TextField()
    seen = models.BooleanField(default=False)

    recipient = models.ForeignKey(UserProfile, related_name="userprofile")
    sender = models.ForeignKey(UserProfile)

    type = models.CharField(max_length=30)

    finished = models.BooleanField(default=False)