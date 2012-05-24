from django.shortcuts import render_to_response, redirect, render
from django.template.context import RequestContext
from account.models import UserProfile, UserDivision
from account.views import user_menu
from division.views import Divisions

def start(request):
    context = user_menu(request)

    user_division = UserDivision.objects.get(user=context['userprofile'])

    divisions = Divisions()
    prev_division, next_division = divisions.next_division(user_division.name)

    context['next_division'] = next_division
    context['prev_division'] = prev_division

    context['avion'] = divisions.get_division_by_name(user_division.name)['plane_type']

    division_users = UserDivision.objects.filter(name=context['division'].name).order_by('points', '-matches_played')

    context['division_users'] = division_users

    return render_to_response('game.html',
                              context,
                              context_instance=RequestContext(request))

