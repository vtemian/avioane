from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import json
import urllib


class Medal(models.Model):

    title = models.CharField(max_length=30)
    type= models.CharField(max_length=30)
    value= models.CharField(max_length=30)
    description= models.CharField(max_length=255)
    image = models.CharField(max_length=50, default='ImagePath')