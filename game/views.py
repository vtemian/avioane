from django.shortcuts import render_to_response, redirect, render
from django.template.context import RequestContext
from account.models import UserProfile, UserDivision
from account.views import user_menu
from division.views import Divisions

def start(request):
    context = user_menu(request)


    divisions = Divisions()
    prev_division, next_division = divisions.next_division(context['division'].name)

    context['next_division'] = next_division
    context['prev_division'] = prev_division

    context['avion'] = divisions.get_division_by_name(context['division'].name)['plane_type']

    division_users = UserDivision.objects.filter(name=context['division'].name).order_by('-points', '-user__lvl', '-matches_played', 'user__user__user__username')

    context['division_users'] = division_users[:5]
    context['my_division'] = divisions.get_division_by_name(context['division'].name)
    remaining_games = context['my_division']['matches'] - context['division'].matches_played
    context['remaining_games'] = remaining_games
    return render_to_response('game.html',
                              context,
                              context_instance=RequestContext(request))

def initiate_new_game(request):
    context = user_menu(request)
    return render_to_response('multiplayer_game.html',
        context,
        context_instance=RequestContext(request))
