from django.shortcuts import render_to_response, redirect, render
from django.template.context import RequestContext
from account.models import UserProfile
from account.views import user_menu

def start(request):
    context = user_menu(request)
    users = UserProfile.objects.all().order_by('-money')[:10]
    context['users'] = users
    print users
    return render_to_response('game.html',
                              context,
                              context_instance=RequestContext(request))

