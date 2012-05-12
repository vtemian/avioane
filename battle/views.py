from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from account.models import UserProfile
from battle.models import Battle, BattleInvitation
from plane.models import Plane, Coordinates, Positioning
from plane.views import check_hit
from nodejs_server.views import send_message
from datetime import datetime as dt
import datetime

def create(firstUser, secondUser):
    try:
        battle = Battle.objects.get(enemy=firstUser, user=secondUser.user, finished=False)
    except Exception:
        try:
            battle = Battle.objects.get(enemy=secondUser, user=firstUser.user, finished=False)
        except Exception:
                battle = Battle.objects.create(enemy=firstUser, user=secondUser.user)

    for x in range(1, 4):
        type = 'plane' + str(x)
        plane, created = Plane.objects.get_or_create(owner=firstUser, battle=battle, type=type)
        plane, created = Plane.objects.get_or_create(owner=secondUser, battle=battle, type=type)

    return battle

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

@csrf_exempt
def send_invitation(request):
    if request.method == 'POST':
        toSimpleUser = User.objects.get(pk=request.POST.get('toUserId'))
        fromUser = request.user

        if fromUser != toSimpleUser:

            toUser = UserProfile.objects.get(user=toSimpleUser)

            #check for battle
            try:
                Battle.objects.get(user=toSimpleUser, finished=False)
                return HttpResponse('battle')
            except Battle.DoesNotExist:
                try:
                    Battle.objects.get(enemy=toUser, finished=False)
                    return HttpResponse('battle')
                except Battle.DoesNotExist:
                    invitations = BattleInvitation.objects.filter(toUser=toUser, finished=False)
                    dont_make_invitation = False
                    for invitation in invitations:
                        print "a"
                        print check_invitation_time(invitation)
                        if check_invitation_time(invitation):
                            invitation.finished = True
                            invitation.save()
                            invitation.delete()
                        else:
                            dont_make_invitation = True
                    print dont_make_invitation
                    if not dont_make_invitation:
                        create_invitation(fromUser, toUser)
                    else:
                        return HttpResponse("not-ready")

                    return HttpResponse("succes")
        else:
            return HttpResponse('duble')
    return HttpResponse('Not here!')

def create_invitation(fromUser, toUser):
    #get or create an invitation
    invitation = BattleInvitation.objects.create(fromUser=fromUser, toUser=toUser)
    print invitation.start_time, dt.now()
    message = '"fromUser": "%s", "toUser": "%s"' % (fromUser.id, toUser.user.id)
    #send to nodejs to realtime send the invitation

    send_message("send-invitation", message)


def check_invitation_time(invitation):
    last_time = invitation.start_time
    this_time = dt.now()
    elapsed = this_time - last_time
    print dir(elapsed)
    print "iuresh", elapsed.seconds / 60 , datetime.timedelta(minutes=1)
    if elapsed.seconds / 60 >= 1    :
        return True
    else:
        return False

@csrf_exempt
def accept_invitation(request):
    if request.method == 'GET':
        firstUser = UserProfile.objects.get(user=request.user)
        secondUser = UserProfile.objects.get(user=User.objects.get(pk=request.GET.get('userid')))
        try:
            invitation = BattleInvitation.objects.get(toUser=firstUser, fromUser=secondUser.user, finished=False)
            if check_invitation_time(invitation):
                invitation.finished = True
                invitation.save()
                invitation.delete()
                return HttpResponse('expired')
            else:
                battle = create(firstUser=firstUser, secondUser=secondUser)
                if battle != 'not-ready':
                    message = '"firstUser": "%s", "secondUser":"%s", "battleId":"%s"' % (firstUser.user.id, secondUser.user.id, battle.id)
                    send_message("new-battle", message)

                    invitation.delete()
                else:
                    return HttpResponse('not-ready')
        except Exception:
            return HttpResponse('bad')

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
        enemyId = request.POST.get('enemy')
        battleId = request.POST.get('battleID')

        userProfile = UserProfile.objects.get(user=request.user)
        enemyUserProfile = UserProfile.objects.get(user=User.objects.get(pk=request.POST.get('enemy')))

        userProfile.ready_for_battle = True
        enemyUserProfile.ready_for_battle = True

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

        enemy = UserProfile.objects.get(user=User.objects.get(pk=request.POST.get('enemy')))
        battle = Battle.objects.get(pk=request.POST.get('battleId'))

        enemy.ready_for_battle = True
        userProfile.ready_for_battle = True

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
    win.won += 1
    loss.money -= 50 - win.lvl
    loss.lost += 1
    win.save()
    loss.save()

@csrf_exempt
def get_details(request):
    try:
        battle = Battle.objects.get(pk=request.GET.get('battleId'))
        user1 = battle.enemy
        user2 = UserProfile.objects.get(user=battle.user)

        return HttpResponse(simplejson.dumps({'user1': {'lvl': user1.lvl, 'username': user1.user.username, 'avion': user1.avion, 'won':user1.won, 'lost':user1.lost}, 'user2': {'lvl': user2.lvl, 'username': user2.user.username, 'avion': user2.avion, 'won':user2.won, 'lost':user2.lost}}))
    except Exception:
        return HttpResponse(simplejson.dumps({'message': 'error'}))