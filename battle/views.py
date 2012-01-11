from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from account.models import UserProfile
from battle.models import Battle

@csrf_exempt
def result(request):
    #TODO: change in POST 
    if request.method == 'POST':
        userProfile = UserProfile.objects.get(user=request.user)
        state = request.POST.get('state')
        
        enemy = UserProfile.objects.get(user=User.objects.get(username=request.POST.get('enemy')))
        battle = Battle.objects.create(user=request.user, enemy=enemy)

        if state == 'loss':
            increase_level(enemy).save()
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
            
    return user

def increase_money(win, loss):
    win.money += 100 + loss.lvl*2
    loss.money -= 50 - win.lvl
    win.save()
    loss.save()