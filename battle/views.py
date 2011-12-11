from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from account.models import UserProfile
from battle.models import Battle

@csrf_exempt
def result(request):
    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)
        state = request.POST.get('state')
        
        enemy = UserProfile.objects.get(user=User.objects.get(username=request.POST.get('enemy')))
        battle = Battle.objects.create(user=user, enemy=enemy)

        if state == 'loss':
            enemy.money += 100
            userProfile.money -= 50
        else:
            userProfile.money += 100
            enemy.money -= 50

        print 'ads'
        
        enemy.save()
        userProfile.save()
        battle.save()
        return HttpResponse('ok')
    return HttpResponse('Not here!')