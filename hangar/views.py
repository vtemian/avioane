__author__ = 'Al'
import hashlib
from django.shortcuts import render_to_response, redirect, render
from django.template.context import RequestContext
from account.models import UserProfile
from account.views import user_menu

from game import views

def hangar(request):
    if request.user.is_authenticated():
        return views.start(request)
    else:
        return render(request, 'login.html')


