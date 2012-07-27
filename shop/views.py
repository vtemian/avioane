
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from account.models import UserStats, UserProfile, UserDivision, UserWeapons, Weapon
from account.views import user_menu
from division.views import Divisions

def shop(request):
    context = user_menu(request)

    return render_to_response('shop.html',
        context,
        context_instance=RequestContext(request))

@csrf_exempt
def items(request):

    user = UserStats.objects.get(user = UserProfile.objects.get(user=request.user))

    division_user = UserDivision.objects.get(user=user)

    my_weapons = UserWeapons.objects.filter(user=division_user)

    divisions = Divisions()

    divisions = divisions.divisions

    what_i_have = []
    what_i_dont_have = []
    what_i_can_buy = []
    what_i_cant_buy = []

    for weapon in my_weapons:
        what_i_have.append(weapon.weapon.name)


    for index, division in  divisions.iteritems():
        for item in division['weapons']:
            if not item in what_i_have:
                what_i_dont_have.append(item)
            if index >= division_user.name:
                what_i_can_buy.append(simplejson.dumps(item))
            else:
                what_i_cant_buy.append(simplejson.dumps(item))

#    what_i_have = simplejson.dumps(what_i_have)
#    what_i_dont_have = simplejson.dumps(what_i_dont_have)
#    what_i_can_buy = simplejson.dumps(what_i_can_buy)
#    what_i_cant_buy = simplejson.dumps(what_i_cant_buy)

    print what_i_cant_buy

    response = simplejson.dumps(
            {
            'what_i_have':what_i_have,
            'what_i_dont_have':what_i_dont_have,
            'what_i_can_buy':what_i_can_buy,
            'what_i_cant_buy':what_i_cant_buy,
        }
    )

    return HttpResponse(response)

@csrf_exempt
def buy(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        user_stats = UserStats.objects.get(user=user_profile)
        user_division = UserDivision.objects.get(user=user_stats)

        item = request.POST.get('item')
        volum = int(request.POST.get('volum'))
        cost = int(request.POST.get('cost'))
        image = request.POST.get('image')
        description = request.POST.get('description')

        total_money = volum * cost

        if total_money and total_money < user_stats.money:
            weapon, created  = Weapon.objects.get_or_create(name=item)

            weapon.image = image
            weapon.description = description
            weapon.save()

            uweapons, created = UserWeapons.objects.get_or_create(weapon=weapon, user=user_division)
            uweapons.qty += volum
            uweapons.save()

            user_stats.money -= total_money
            user_stats.save()

            return HttpResponse('ok')

        else:
            return HttpResponse('money')
    return HttpResponse('not-here')