from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from account.models import UserProfile, UserStats, UserDivision, UserMedals
from battle.models import Battle, BattleInvitation
from division.views import Divisions
from plane.models import Plane, Coordinates, Positioning
from plane.views import check_hit
from nodejs_server.views import send_message
from datetime import datetime as dt, timedelta
import datetime
from medals.models import Medal

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
def get_badge(badge_type ,user):

    try:
        stats = UserStats.objects.get(user=user)
        badge= Medal.objects.get(type=badge_type)
        medals=UserMedals.objects.filter(user=stats)
        exist=0
        for medal in medals:
            if medal.medals == badge.pk:
                exist=1
        if exist==0:
            succes= UserMedals.objects.create(user= stats, medals=badge)
            succes.save()
        return HttpResponse(simplejson.dumps({'ok': '/'}))
    except Exception as exp:
        print exp.message
        return HttpResponse(simplejson.dumps({'ok': '/'}))
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
    return (this_time -last_time) > timedelta (minutes = 1)

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

        division = Divisions()
        division.check_division(userProfile, enemyUserProfile)


        battle.finished = True
        battle.save()

    return HttpResponse('Not here!')

@csrf_exempt
def result(request):
    if request.method == 'POST':
        try:
            userProfile = UserProfile.objects.get(user=request.user)
            state = request.POST.get('state')

            enemy = UserProfile.objects.get(user=User.objects.get(pk=request.POST.get('enemy')))
            battle = Battle.objects.get(pk=request.POST.get('battleId'), finished=False)

            enemy.ready_for_battle = True
            userProfile.ready_for_battle = True

            #finished the battle
            battle.finished = True

            if state == 'loss':
                increase_level(enemy)
                increase_money(enemy, userProfile)

                division = Divisions()
                division.check_division(enemy, userProfile)

            enemy.save()
            userProfile.save()
            battle.save()
            return HttpResponse('ok')
        except Exception as ext:
            print ext.message
    return HttpResponse('Not here!')


def increase_level(user):
    user = UserStats.objects.get(user=user)
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
    win = UserStats.objects.get(user=win)
    loss = UserStats.objects.get(user=loss)

    win.money += 100 + loss.lvl*2
    win.won += 1

    loss.money -= 50 - win.lvl
    if loss.money < 0:
        loss.money = 0
    loss.lost += 1

    win.save()
    loss.save()

@csrf_exempt
def get_details(request):
    try:
        battle = Battle.objects.get(pk=request.GET.get('battleId'))
        user1 = UserStats.objects.get(user=battle.enemy)
        user2 = UserStats.objects.get(user=UserProfile.objects.get(user=battle.user))
        user_division1 = UserDivision.objects.get(user=user1)
        user_division2 = UserDivision.objects.get(user=user2)
        divisions = Divisions()
        avion1 = divisions.get_division_by_name(user_division1.name)['plane_type']
        avion2 = divisions.get_division_by_name(user_division2.name)['plane_type']
        return HttpResponse(simplejson.dumps({'user1': {'lvl': user1.lvl, 'username': user1.user.user.username, 'avion': avion1, 'won':user1.won, 'lost':user1.lost}, 'user2': {'lvl': user2.lvl, 'username': user2.user.user.username, 'avion': avion2, 'won':user2.won, 'lost':user2.lost}}))
    except Exception as exp:
        print exp.message
        return HttpResponse(simplejson.dumps({'message': 'error'}))

@csrf_exempt
def lost_planes_position(request):
    if request.method == 'POST':
        userProfile = UserProfile.objects.get(user=request.user)

        enemy = UserProfile.objects.get(user=User.objects.get(pk=request.POST.get('enemy')))
        battle = Battle.objects.get(pk=request.POST.get('battleId'))

        enemy.ready_for_battle = True
        userProfile.ready_for_battle = True

        #finished the battle
        battle.finished = True

        increase_level(enemy)
        increase_money(enemy, userProfile)

        division = Divisions()
        division.check_division(enemy, userProfile)

        enemy.save()
        userProfile.save()
        battle.save()
        return HttpResponse('ok')
    return HttpResponse('Not here!')
