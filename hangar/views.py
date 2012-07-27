import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from account.models import UserWeapons, UserDivision, UserStats, UserProfile
from division.views import Divisions

from django.shortcuts import render_to_response, redirect, render
from django.template.context import RequestContext
from account.views import user_menu


def hangar(request):
    context = user_menu(request)

    divisions = Divisions()
    context['avion'] = divisions.get_division_by_name(context['division'].name)['plane_type']

    user_division = UserDivision.objects.get(user=context['userprofile'])

    weapons = UserWeapons.objects.filter(user=user_division)

    context['max_load'] = divisions.get_division_by_name(context['division'].name)['max_weapons']

    context['weapons'] = weapons
    context['use_weapons'] = weapons.filter(on=True)

    return render_to_response('hangar.html',
        context,
        context_instance=RequestContext(request))

@csrf_exempt
def equip(request):
    if request.method == "POST":
        user = UserStats.objects.get(user = UserProfile.objects.get(user=request.user))

        division_user = UserDivision.objects.get(user=user)
        divisions = Divisions()

        my_division = divisions.get_division_by_name(division_user.name)
        my_weapon = UserWeapons.objects.get(weapon__name = request.POST.get('name'), user=division_user)

        if not my_weapon.on:

            max_weapon = my_division['max_weapons']

            my_weapons = UserWeapons.objects.filter(user=division_user, on=True).count()

            if my_weapons < max_weapon:
                my_weapon.on = True
                my_weapon.save()
                return HttpResponse('ok')
            else:
                return HttpResponse('many')
        else:
            return HttpResponse('on')

    return HttpResponse('NOt here!')
@csrf_exempt
def dequip(request):
    if request.method == "POST":
        user = UserStats.objects.get(user = UserProfile.objects.get(user=request.user))

        division_user = UserDivision.objects.get(user=user)
        divisions = Divisions()

        my_division = divisions.get_division_by_name(division_user.name)
        my_weapon = UserWeapons.objects.get(weapon__name = request.POST.get('name'), user=division_user)

        if my_weapon.on:
            my_weapon.on = False
            my_weapon.save()
            return HttpResponse('ok')
        else:
            return HttpResponse('not')

    return HttpResponse('NOt here!')

@csrf_exempt
def get_wepons(request):
    user = UserStats.objects.get(user = UserProfile.objects.get(user=request.user))

    division_user = UserDivision.objects.get(user=user)

    weapons = UserWeapons.objects.filter(user=division_user, on=True, qty__gt=3)

    my_weapons = []

    for weapon in weapons:
        print weapon
        my_weapons.append(
                {
                    'name': weapon.weapon.name,
                    'image': weapon.weapon.image,
                    'qty': weapon.qty,
                }
        )

    return HttpResponse(simplejson.dumps({'weapons':my_weapons}))

