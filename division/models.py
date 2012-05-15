__author__ = 'Al'
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import json
import urllib

class division(models.Model):
    name=models.CharField(max_length=30, default='D')
