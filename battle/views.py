from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from account.models import UserProfile
from battle.models import Battle
from plane.models import Plane, Coordinates, Positioning
from plane.views import check_hit

@csrf_exempt
def create(request):
    if request.method == 'POST':
        user = UserProfile.objects.get(user=request.user)
        enemy = UserProfile.objects.get(user=User.objects.get(username=request.POST.get('enemy')))
        
        try:
            battle = Battle.objects.get(enemy=enemy, user=request.user, finished=False)
        except Battle.DoesNotExist:
            try:
                battle = Battle.objects.get(enemy=user, user=enemy.user, finished=False)
            except Battle.DoesNotExist:
                battle = Battle.objects.create(enemy=enemy, user=request.user)
                
        return HttpResponse(battle.id)
    return HttpResponse('Not here!')

@csrf_exempt
def attack(request):
    if request.method == 'POST':
        #get data from post
        x = request.POST.get('x')
        y = request.POST.get('y')
        battle = Battle.objects.get(pk=request.POST.get('battleID'))
        user = UserProfile.objects.get(user=request.user)
        types = ['plane1', 'plane2', 'plane3']
        
        for type in types:
            plane = Plane.objects.get(battle=battle, owner=user, type=type)
            result = check_hit(plane, x, y)
            #checking for the result: head, hit, False
            if result == 'head':
                if check_finished(battle, user, type):
                    return HttpResponse('finished')
                else:
                    plane.dead = True
                    plane.save()
                    return HttpResponse(type)
            else:
                if result:
                    return HttpResponse(result)
        return HttpResponse('miss')
    
    return HttpResponse('Not here!')

def check_finished(battle, owner, type):
    types = ['plane1', 'plane2', 'plane3']
    k = 0
    
    for thisType in types:
        if thisType != type:
            plane = Plane.objects.get(battle=battle, owner=owner, type=thisType)
            if plane.dead:
                k += 1
    print k
    if k == 2:
        return True
    return False

@csrf_exempt
def disconnect(request):
    if request.method == 'POST':
        #Get POST values
        enemyName = request.POST.get('enemy')
        battleId = request.POST.get('battleID')

        userProfile = UserProfile.objects.get(user=request.user)
        enemyUserProfile = UserProfile.objects.get(user__username=enemyName)
        battle = Battle.objects.get(pk=battleId)

        increase_level(userProfile)
        increase_money(userProfile, enemyUserProfile)

        battle.finished = True
        battle.save()

    return HttpResponse('Not here!')

@csrf_exempt
def result(request):
    if request.method == 'POST':
        userProfile = UserProfile.objects.get(user=request.user)
        state = request.POST.get('state')
        
        enemy = UserProfile.objects.get(user=User.objects.get(username=request.POST.get('enemy')))
        battle = Battle.objects.get(user=request.user, enemy=enemy)

        #finished the battle
        battle.finished = True
        
        if state == 'loss':
            increase_level(enemy)
            increase_money(enemy, userProfile)

        enemy.save()
        userProfile.save()
        battle.save()
        return HttpResponse('ok')
    return HttpResponse('Not here!')


def increase_level(user):
    if user.lvl == 1:
        user.lvl += 1
    else:
        #TODO: formula pentru lvl
        exp = user.lvl * user.lvl + user.lvl * 2
        user.exp += exp
        if user.exp >= user.lvl * user.lvl * user.lvl *5:
            user.lvl += 1
    user.save()

def increase_money(win, loss):
    win.money += 100 + loss.lvl*2
    loss.money -= 50 - win.lvl
    win.save()
    loss.save()